from typing import Optional, Dict
from pydantic import BaseModel, Field

class Stock(BaseModel):
    afterHours: Optional[float] = Field(None)
    close: float
    from_: str = Field(..., alias="from")
    high: float
    low: float
    open: float
    preMarket: Optional[float] = Field(None)
    status: str
    symbol: str
    volume: int
    performance: Dict = Field(default_factory=dict)
    amount: int = 0


class Config:
    allow_population_by_field_name = True
    schema_extra = {
        "example": {
            "afterHours": 100.5,
            "close": 99.8,
            "from": "2025-09-12",
            "high": 101.2,
            "low": 98.4,
            "open": 99.0,
            "preMarket": 100.0,
            "status": "OK",
            "symbol": "AAPL",
            "volume": 1200000,
            "performance": {"1d": "+1.2%"},
            "amount": 0,
        }
    }

class AmountIn(BaseModel):
    amount: int