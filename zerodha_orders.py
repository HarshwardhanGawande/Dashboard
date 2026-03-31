import requests
import json
import pandas as pd
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from typing import Literal, Optional
import os

load_dotenv(override=True)

# ─── Config ──────────────────────────────────────────────────────────────────

USER_ID  = os.getenv('USER_ID')
PASSWORD = os.getenv('ZERODHA_PASSWORD')
ENCTOKEN = os.getenv('ENCTOKEN')

BASE_URL  = 'https://kite.zerodha.com'
LOGIN_URL = f'{BASE_URL}/api/login'
TWOFA_URL = f'{BASE_URL}/api/twofa'
HIST_URL  = f'{BASE_URL}/oms/instruments/historical/{{instrument_id}}/{{interval}}'

# ─── Base Class ───────────────────────────────────────────────────────────────

class ZerodhaBase:

    def __init__(self):
        global ENCTOKEN
        self.user_id  = USER_ID
        self.password = PASSWORD
        self.enctoken = ENCTOKEN
        self.session  = requests.Session()
        self._set_headers()

    def _set_headers(self):
        self.session.headers.update({
            'authorization': f'enctoken {self.enctoken}',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

    def _save_enctoken(self, enctoken: str):
        env_lines = []
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_lines = f.readlines()
        env_lines = [l for l in env_lines if not l.startswith('ENCTOKEN=')]
        env_lines.append(f'ENCTOKEN={enctoken}\n')
        with open('.env', 'w') as f:
            f.writelines(env_lines)

    def _login(self):
        global ENCTOKEN
        r = self.session.post(LOGIN_URL, data={
            'user_id': self.user_id,
            'password': self.password,
        })
        request_id = r.json()['data']['request_id']

        twofa_value = input('Enter 2FA value: ')
        self.session.post(TWOFA_URL, data={
            'user_id': self.user_id,
            'request_id': request_id,
            'twofa_value': twofa_value,
        })

        self.enctoken = requests.utils.dict_from_cookiejar(self.session.cookies)['enctoken']
        ENCTOKEN = self.enctoken
        print(f'New ENCTOKEN: {self.enctoken}')

        self._save_enctoken(self.enctoken)
        self._set_headers()   # update session headers with new token

    def test_validity(self):
        """Check token validity; re-login if expired."""
        print(f'Checking token: {self.enctoken}')
        resp = self.session.get(
            url=HIST_URL.format(instrument_id=86529, interval='minute'),
            params={'user_id': self.user_id, 'oi': '1',
                    'from': '2026-03-25', 'to': '2026-03-25'},
        )
        if resp.status_code != 200:
            print(f"Token expired: {resp.json().get('message')} — logging in...")
            self._login()
        else:
            print('Token valid.')


# ─── Orders Class ─────────────────────────────────────────────────────────────

class ZerodhaIntraday(ZerodhaBase):

    ORDER_URL = f'{BASE_URL}/oms/orders'

    def __init__(self):
        super().__init__()
        self.test_validity()   # auto-check token on init

    def _place_order(self, variety: str, payload: dict) -> dict:
        if self.user_id:
            payload['user_id'] = self.user_id
        response = self.session.post(f'{self.ORDER_URL}/{variety}', data=payload)
        response.raise_for_status()
        return response.json()

    def _base_payload(self, tradingsymbol, exchange, transaction_type, quantity):
        return {
            'exchange': exchange,
            'tradingsymbol': tradingsymbol,
            'transaction_type': transaction_type,
            'quantity': quantity,
            'product': 'MIS',
            'validity': 'DAY',
            'tag': 'tfc_tv',
        }

    def market(self, tradingsymbol: str, transaction_type: Literal['BUY', 'SELL'],
               quantity: int, exchange: str = 'NSE') -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'regular', 'order_type': 'MARKET',
            'price': 0, 'trigger_price': 0, 'disclosed_quantity': 0,
            'squareoff': 0, 'stoploss': 0, 'trailing_stoploss': 0,
        })
        return self._place_order('regular', payload)

    def limit(self, tradingsymbol: str, transaction_type: Literal['BUY', 'SELL'],
              quantity: int, price: float, exchange: str = 'NSE') -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'regular', 'order_type': 'LIMIT',
            'price': price, 'trigger_price': 0, 'disclosed_quantity': 0,
            'squareoff': 0, 'stoploss': 0, 'trailing_stoploss': 0,
        })
        return self._place_order('regular', payload)

    def cover_market(self, tradingsymbol: str, transaction_type: Literal['BUY', 'SELL'],
                     quantity: int, trigger_price: float, exchange: str = 'NSE') -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'co', 'order_type': 'MARKET',
            'price': 0, 'trigger_price': trigger_price,
        })
        return self._place_order('co', payload)

    def cover_limit(self, tradingsymbol: str, transaction_type: Literal['BUY', 'SELL'],
                    quantity: int, price: float, trigger_price: float,
                    exchange: str = 'NSE') -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'co', 'order_type': 'LIMIT', 'product': 'CO',
            'price': price, 'trigger_price': trigger_price,
        })
        return self._place_order('co', payload)


# ─── Data Class ───────────────────────────────────────────────────────────────

class ZerodhaData(ZerodhaBase):

    CHUNK_DAYS = 1825

    nifty_dict = {
        "M&M": 519937, "ETERNAL": 1304833, "EICHERMOT": 232961,
        "SHRIRAMFIN": 1102337, "INDIGO": 2865921, "ADANIENT": 6401,
        "BAJFINANCE": 81153, "TMPV": 884737, "LT": 2939649,
        "TRENT": 502785, "BAJAJ-AUTO": 4267265, "HINDALCO": 348929,
        "TITAN": 897537, "SBIN": 779521, "TATASTEEL": 895745,
        "ADANIPORTS": 3861249, "JIOFIN": 4644609, "BAJAJFINSV": 4268801,
        "SUNPHARMA": 857857, "DRREDDY": 225537, "MARUTI": 2815745,
        "BHARTIARTL": 2714625, "APOLLOHOSP": 40193, "ICICIBANK": 1270529,
        "HINDUNILVR": 356865, "AXISBANK": 1510401, "RELIANCE": 738561,
        "KOTAKBANK": 492033, "JSWSTEEL": 3001089, "SBILIFE": 5582849,
        "ITC": 424961, "GRASIM": 315393, "MAXHEALTH": 5728513,
        "BEL": 98049, "HDFCBANK": 341249, "ASIANPAINT": 60417,
        "ULTRACEMCO": 2952193, "COALINDIA": 5215745, "POWERGRID": 3834113,
        "CIPLA": 177665, "HDFCLIFE": 119553, "WIPRO": 969473,
        "NTPC": 2977281, "TCS": 2953217, "TATACONSUM": 878593,
        "NESTLEIND": 4598529, "ONGC": 633601, "INFY": 408065,
        "TECHM": 3465729, "HCLTECH": 1850625, "NIFTY 50": 256265,
    }

    def __init__(self):
        super().__init__()

    def _fetch_chunk(self, tickers: list, from_str: str, to_str: str, interval: str) -> pd.DataFrame:
        params   = {'user_id': self.user_id, 'oi': '1', 'from': from_str, 'to': to_str}
        chunk_df = None

        for ticker in tickers:
            instrument_id = self.nifty_dict.get(ticker)
            if not instrument_id:
                raise ValueError(f'Unknown ticker: {ticker}')

            url  = HIST_URL.format(instrument_id=instrument_id, interval=interval)
            resp = self.session.get(url=url, params=params)
            data = resp.json()
            print(f'{ticker} [{instrument_id}] — {data.get("status")} ({resp.status_code})')

            if data.get('status') != 'success':
                raise RuntimeError(f"Error fetching {ticker}: {data.get('message', 'Unknown error')}")

            df = (
                pd.DataFrame(data['data']['candles'])
                  .iloc[:, [0, 4]]
                  .set_index(0)
                  .rename(columns={4: ticker})
            )
            chunk_df = df if chunk_df is None else chunk_df.join(df)

        return chunk_df

    def load_data(self, tickers: list, from_date: str, interval: str = 'day') -> pd.DataFrame:
        self.test_validity()

        from_dt = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_dt   = date.today()
        to_str  = to_dt.strftime('%Y-%m-%d')
        main_df = None

        if (to_dt - from_dt).days > self.CHUNK_DAYS:
            current_from = from_dt
            while current_from < to_dt:
                chunk_to = min(current_from + timedelta(days=self.CHUNK_DAYS), to_dt)
                print(f'Fetching chunk: {current_from} → {chunk_to}')
                chunk_df = self._fetch_chunk(tickers, current_from.strftime('%Y-%m-%d'),
                                             chunk_to.strftime('%Y-%m-%d'), interval)
                main_df  = chunk_df if main_df is None else pd.concat([main_df, chunk_df]).sort_index()
                current_from = chunk_to + timedelta(days=1)
        else:
            print(f'Fetching: {from_date} → {to_str}')
            main_df = self._fetch_chunk(tickers, from_date, to_str, interval)

        main_df.index.name = 'Date'
        return main_df