import os
import httpx
from datetime import datetime, timedelta, date
from typing import Any, Dict, Optional


POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")
BASE = "https://api.polygon.io"


def _ensure_key() -> None:
    if not POLYGON_API_KEY:
        raise RuntimeError("POLYGON_API_KEY environment variable not set")


def _previous_workday(d: date) -> date:
    """Return the most recent weekday before `d` (skip Sat/Sun)."""
    while d.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        d -= timedelta(days=1)
    return d


async def __request_polygon_data(symbol: str, target_date: date) -> Dict[str, Any]:
    url = f"{BASE}/v1/open-close/{symbol}/{target_date}"
    params = {"adjusted": "true", "apiKey": POLYGON_API_KEY}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_polygon_data(symbol: str) -> Dict[str, Optional[Any]]:
    _ensure_key()
    symbol = symbol.upper()

    target_date = _previous_workday(date.today())
    data = await __request_polygon_data(symbol, target_date)

    # Handle case where today's data is not yet available
    if "message" in data and "before end of day" in data["message"].lower():
        prev_day = _previous_workday(target_date - timedelta(days=1))
        data = await __request_polygon_data(symbol, prev_day)

    mapped: Dict[str, Optional[Any]] = {
        "afterHours": float(data["afterHours"]) if data.get("afterHours") is not None else None,
        "close": float(data["close"]),
        "from": data.get("from") or str(target_date),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "open": float(data["open"]),
        "preMarket": float(data["preMarket"]) if data.get("preMarket") is not None else None,
        "status": data.get("status", "OK"),
        "volume": int(data["volume"]),
    }

    return mapped