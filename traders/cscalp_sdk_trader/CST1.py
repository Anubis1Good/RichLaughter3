import time
import requests
import pandas as pd
from typing import List, Optional, Dict, Any


class CscalpServerError(Exception):
    """Ошибка, возвращенная локальным C#-сервером."""
    pass


class CscalpClient:
    def __init__(self, base_url: str = "http://localhost:7777", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # Используем Session для переиспользования TCP-соединений (Keep-Alive) — запросы будут идти < 1 мс
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        data = resp.json()
        if resp.status_code >= 400:
            raise CscalpServerError(data.get("error", f"HTTP {resp.status_code}: {data}"))
        return data

    # --- Управление и подписка ---

    def status(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/status")

    def wait_until_ready(self, slots: List[str], timeout_sec: float = 30.0) -> None:
        """Ожидает готовности всех указанных слотов при старте робота."""
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            statuses = {s["alias"]: s["isReady"] for s in self.status()}
            if all(statuses.get(slot, False) for slot in slots):
                return
            time.sleep(0.5)
        raise TimeoutError(f"Слоты {slots} не перешли в состояние Ready за {timeout_sec} сек.")

    def subscribe(self, slot: str, tickers: List[str]) -> Dict[str, str]:
        return self._request("POST", "/subscribe", json={"slot": slot, "tickers": tickers})

    # --- Рыночные данные ---

    def get_best_prices(self, slot: str, ticker: str) -> Dict[str, Any]:
        return self._request("GET", "/best-prices", params={"slot": slot, "ticker": ticker})

    def get_orderbook(self, slot: str, ticker: str, depth: int = 20) -> Dict[str, Any]:
        return self._request("GET", "/orderbook", params={"slot": slot, "ticker": ticker, "depth": depth})

    def get_candles(self, slot: str, ticker: str, tf_minutes: int = 5, limit: int = 200) -> pd.DataFrame:
        data = self._request("GET", "/candles", params={
            "slot": slot,
            "ticker": ticker,
            "tf_minutes": tf_minutes,
            "limit": limit
        })
        df = pd.DataFrame(data)
        if not df.empty and "time" in df.columns:
            # Убираем суффикс Z, так как сервер отдаёт биржевое время (МСК)
            df["time"] = pd.to_datetime(df["time"].astype(str).str.rstrip("Z"))
        return df

    def get_ticks(self, slot: str, ticker: str, limit: int = 500) -> pd.DataFrame:
        data = self._request("GET", "/ticks", params={"slot": slot, "ticker": ticker, "limit": limit})
        df = pd.DataFrame(data)
        if not df.empty and "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"].astype(str).str.rstrip("Z"))
        return df

    def get_clusters(self, slot: str, ticker: str, tf_minutes: int = 5, limit: int = 50) -> List[Dict[str, Any]]:
        return self._request("GET", "/clusters", params={
            "slot": slot,
            "ticker": ticker,
            "tf_minutes": tf_minutes,
            "limit": limit
        })

    # --- Позиция и торговля ---

    def get_position(self, slot: str, ticker: str) -> Dict[str, Any]:
        return self._request("GET", "/position", params={"slot": slot, "ticker": ticker})

    def get_orders(self, slot: str, ticker: str) -> Dict[str, List[Dict[str, Any]]]:
        return self._request("GET", "/orders", params={"slot": slot, "ticker": ticker})

    def buy_limit(self, slot: str, ticker: str, amount: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Если price=None, сервер сам встанет лучшим покупателем (или вместе с лучшим в спред)."""
        return self._request("POST", "/order", json={
            "slot": slot,
            "ticker": ticker,
            "side": "BUY",
            "amount": amount,
            "price": price
        })

    def sell_limit(self, slot: str, ticker: str, amount: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Если price=None, сервер сам встанет лучшим продавцом (или вместе с лучшим в спред)."""
        return self._request("POST", "/order", json={
            "slot": slot,
            "ticker": ticker,
            "side": "SELL",
            "amount": amount,
            "price": price
        })

    def cancel(self, slot: str, ticker: str, order_id: Optional[str] = None) -> Dict[str, Any]:
        """Если order_id=None, снимает все активные заявки по инструменту."""
        return self._request("POST", "/cancel", json={
            "slot": slot,
            "ticker": ticker,
            "orderId": order_id
        })
