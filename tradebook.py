# ─── Console Class ────────────────────────────────────────────────────────────
from zerodha_orders import ZerodhaBase
from datetime import date
import pandas as pd
from datetime import date
from typing import  Optional

CONSOLE_BASE_URL  = 'https://console.zerodha.com'
TRADEBOOK_URL     = f'{CONSOLE_BASE_URL}/api/reports/tradebook'
CONSOLE_HEADERS   = lambda enctoken: {
    'authorization': f'enctoken {enctoken}',
    'referer':       f'{CONSOLE_BASE_URL}/',
    'origin':        CONSOLE_BASE_URL,
}

class ZerodhaConsole(ZerodhaBase):

    def __init__(self):
        super().__init__()
        self.test_validity()

    def _console_get(self, url: str, params: dict) -> dict:
        """Authenticated GET to console.zerodha.com — raises on non-success."""
        resp = self.session.get(url, params=params, headers=CONSOLE_HEADERS(self.enctoken))

        if resp.status_code != 200:
            raise RuntimeError(
                f"Console request failed (HTTP {resp.status_code}): {resp.text[:300]}"
            )

        body = resp.json()
        if body.get('status') != 'success':
            raise RuntimeError(f"Console API error: {body.get('message', body)}")

        return body['data']

    def get_tradebook(
        self,
        from_date: str,
        to_date:   Optional[str] = None,
        segment:   str = 'EQ',
        sort_by:   str = 'order_execution_time',
        sort_desc: bool = False,
        all_pages: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch tradebook from Zerodha Console for a date range.

        Args:
            from_date:  Start date 'YYYY-MM-DD'.
            to_date:    End date 'YYYY-MM-DD'. Defaults to today.
            segment:    'EQ', 'FO', 'COM', 'MF', etc.
            sort_by:    Column to sort by.
            sort_desc:  Descending sort if True.
            all_pages:  Auto-paginate and return all records if True.

        Returns:
            pd.DataFrame of all tradebook rows.
        """
        if to_date is None:
            to_date = date.today().strftime('%Y-%m-%d')

        params = {
            'segment':   segment,
            'from_date': from_date,
            'to_date':   to_date,
            'sort_by':   sort_by,
            'sort_desc': str(sort_desc).lower(),
            'page':      1,
        }

        all_records = []

        while True:
            data       = self._console_get(TRADEBOOK_URL, params)
            records    = data.get('result', [])
            pagination = data.get('pagination', {})

            all_records.extend(records)

            total_pages = pagination.get('total_pages', 1)
            current     = pagination.get('page', params['page'])
            total       = pagination.get('total', len(all_records))

            print(f"  Page {current}/{total_pages}: {len(records)} records "
                  f"(fetched: {len(all_records)}/{total})")

            if not all_pages or current >= total_pages:
                break

            params['page'] += 1

        df = pd.DataFrame(all_records)
        if not df.empty:
            df['order_execution_time'] = pd.to_datetime(df['order_execution_time'])
            df['trade_date']           = pd.to_datetime(df['trade_date']).dt.date
        return df

    def get_tradebook_by_symbol(
        self,
        tradingsymbol: str,
        from_date:     str,
        to_date:       Optional[str] = None,
        segment:       str = 'EQ',
    ) -> pd.DataFrame:
        """Convenience wrapper — fetches full tradebook then filters by symbol."""
        df = self.get_tradebook(from_date, to_date, segment)
        return df[df['tradingsymbol'] == tradingsymbol].reset_index(drop=True)

    def get_pnl_summary(
        self,
        from_date: str,
        to_date:   Optional[str] = None,
        segment:   str = 'EQ',
    ) -> pd.DataFrame:
        """
        Aggregates tradebook into a per-symbol P&L summary.

        Rolls up all fills per order_id first (weighted avg price, total qty),
        then pairs buys vs sells using FIFO to compute realised P&L.

        Returns:
            pd.DataFrame with columns:
                tradingsymbol, total_buy_qty, avg_buy_price,
                total_sell_qty, avg_sell_price, realised_pnl
        """
        df = self.get_tradebook(from_date, to_date, segment)
        if df.empty:
            return df

        # ── Step 1: roll up multiple fills per order_id ───────────────────────
        df['value'] = df['price'] * df['quantity']

        orders = (
            df.groupby(['order_id', 'tradingsymbol', 'trade_type', 'trade_date'])
              .agg(quantity=('quantity', 'sum'), value=('value', 'sum'))
              .reset_index()
        )
        orders['avg_price'] = orders['value'] / orders['quantity']

        # ── Step 2: split buys and sells ──────────────────────────────────────
        buys  = orders[orders['trade_type'] == 'buy']
        sells = orders[orders['trade_type'] == 'sell']

        rows = []
        for symbol in orders['tradingsymbol'].unique():
            b = buys[buys['tradingsymbol'] == symbol]
            s = sells[sells['tradingsymbol'] == symbol]

            total_buy_qty   = b['quantity'].sum()
            total_sell_qty  = s['quantity'].sum()
            avg_buy_price   = (b['value'].sum()  / total_buy_qty)  if total_buy_qty  else 0
            avg_sell_price  = (s['value'].sum()  / total_sell_qty) if total_sell_qty else 0

            matched_qty   = min(total_buy_qty, total_sell_qty)
            realised_pnl  = (avg_sell_price - avg_buy_price) * matched_qty if matched_qty else 0

            rows.append({
                'tradingsymbol':  symbol,
                'total_buy_qty':  total_buy_qty,
                'avg_buy_price':  round(avg_buy_price,  4),
                'total_sell_qty': total_sell_qty,
                'avg_sell_price': round(avg_sell_price, 4),
                'matched_qty':    matched_qty,
                'realised_pnl':   round(realised_pnl,   2),
            })

        return pd.DataFrame(rows).sort_values('realised_pnl', ascending=False).reset_index(drop=True)


# console = ZerodhaConsole()
# console._login()

# Full tradebook for a date range
# tb = console.get_tradebook('2026-03-01')

# # Filter to a single stock
# tmcv = console.get_tradebook_by_symbol('TMCV', '2026-03-01')

# Rolled-up P&L summary across all symbols
from zerodha_orders import ZerodhaIntraday

z = ZerodhaIntraday()

# full order book
orders = z.order_list()

# filter by symbol
# orders_sb = z.order_list(tradingsymbol='SBIN')

# filter by status
open_orders = z.order_list(status='OPEN')
print(open_orders)