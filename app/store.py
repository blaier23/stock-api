from collections import defaultdict
from threading import Lock

class StockStore:
    def __init__(self):
        self._amounts = defaultdict(int)
        self._lock = Lock()

    def get_amount(self, symbol: str) -> int:
        return int(self._amounts.get(symbol.upper(), 0))


    def add_amount(self, symbol: str, amount: int) -> None:
        symbol = symbol.upper()
        with self._lock:
            self._amounts[symbol] = int(self._amounts.get(symbol, 0)) + int(amount)


STOCK_STORE = StockStore()