import requests
from typing import Literal, Optional
from dotenv import load_dotenv
import os

load_dotenv()

class ZerodhaIntraday:

    BASE_URL = 'https://kite.zerodha.com/oms/orders'

    def __init__(self):
        enctoken = os.getenv('ZERODHA_ENCTOKEN')
        if not enctoken:
            raise ValueError("ZERODHA_ENCTOKEN not found in .env file")

        self.user_id = os.getenv('ZERODHA_USER_ID')
        self.session = requests.Session()
        self.session.headers.update({
            'authorization': f'enctoken {enctoken}',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

    def _place_order(self, variety: str, payload: dict) -> dict:
        if self.user_id:
            payload['user_id'] = self.user_id
        response = self.session.post(f'{self.BASE_URL}/{variety}', data=payload)
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

    def market(
        self,
        tradingsymbol: str,
        transaction_type: Literal['BUY', 'SELL'],
        quantity: int,
        exchange: str = 'NSE',
    ) -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'regular',
            'order_type': 'MARKET',
            'price': 0,
            'trigger_price': 0,
            'disclosed_quantity': 0,
            'squareoff': 0,
            'stoploss': 0,
            'trailing_stoploss': 0,
        })
        return self._place_order('regular', payload)

    def limit(
        self,
        tradingsymbol: str,
        transaction_type: Literal['BUY', 'SELL'],
        quantity: int,
        price: float,
        exchange: str = 'NSE',
    ) -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'regular',
            'order_type': 'LIMIT',
            'price': price,
            'trigger_price': 0,
            'disclosed_quantity': 0,
            'squareoff': 0,
            'stoploss': 0,
            'trailing_stoploss': 0,
        })
        return self._place_order('regular', payload)

    def cover_market(
        self,
        tradingsymbol: str,
        transaction_type: Literal['BUY', 'SELL'],
        quantity: int,
        trigger_price: float,
        exchange: str = 'NSE',
    ) -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'co',
            'order_type': 'MARKET',
            'price': 0,
            'trigger_price': trigger_price,
        })
        return self._place_order('co', payload)

    def cover_limit(
        self,
        tradingsymbol: str,
        transaction_type: Literal['BUY', 'SELL'],
        quantity: int,
        price: float,
        trigger_price: float,
        exchange: str = 'NSE',
    ) -> dict:
        payload = self._base_payload(tradingsymbol, exchange, transaction_type, quantity)
        payload.update({
            'variety': 'co',
            'order_type': 'LIMIT',
            'product': 'CO',
            'price': price,
            'trigger_price': trigger_price,
        })
        return self._place_order('co', payload)


# ─── Usage ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    z = ZerodhaIntraday()

    # Regular Market Order
    res = z.market('IDEA', 'BUY', quantity=1)
    print(res)

    # Regular Limit Order
    res = z.limit('RVNL', 'BUY', quantity=1, price=255)
    print(res)

    # Cover Market Order
    res = z.cover_market('RVNL', 'BUY', quantity=1, trigger_price=247)
    print(res)

    # Cover Limit Order
    res = z.cover_limit('RVNL', 'BUY', quantity=1, price=250, trigger_price=249)
    print(res)