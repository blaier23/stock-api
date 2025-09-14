import asyncio
from fastapi import FastAPI, HTTPException, Path
from pydantic import ValidationError
from starlette.responses import JSONResponse
from logging import getLogger

from app.models import Stock, AmountIn
from app.services.polygon import fetch_polygon_data
from app.services.marketwatch import fetch_marketwatch_performance
from app.store import STOCK_STORE

app = FastAPI(title="Stock API")

logger = getLogger(__name__)

@app.get("/")
def root():
    return {"message": "Running"}

@app.get("/stock/{symbol}", response_model=Stock)
async def get_stock(symbol: str = Path(..., description="Stock symbol (e.g. AAPL)")):
    symbol = symbol.upper()

    try:
        # Run Polygon + Marketwatch concurrently
        poly_task = asyncio.create_task(fetch_polygon_data(symbol))
        perf_task = asyncio.create_task(fetch_marketwatch_performance(symbol))
        poly, perf = await asyncio.gather(poly_task, perf_task)
    except Exception as e:
        # Logging
        logger.error(f"Error fetching data for {symbol}")
        raise HTTPException(status_code=502, detail=f"Error fetching data for {symbol}")

    amount = STOCK_STORE.get_amount(symbol)

    stock_obj = {
        "afterHours": poly.get("afterHours"),
        "close": poly.get("close"),
        "from": poly.get("from"),
        "high": poly.get("high"),
        "low": poly.get("low"),
        "open": poly.get("open"),
        "preMarket": poly.get("preMarket"),
        "status": poly.get("status"),
        "symbol": symbol,
        "volume": poly.get("volume"),
        "performance": perf,
        "amount": amount,
    }

    try:
        stock = Stock(**stock_obj)

    except ValidationError as e:
        raise HTTPException(status_code=502, detail=f"Invalid data from sources: {e}")

    return stock

@app.post("/stock/{symbol}")
async def post_stock(symbol: str, amount_in: AmountIn):
    symbol = symbol.upper()
    amount = amount_in.amount

    # TODO: Validate symbol by fetching data from Polygon
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    STOCK_STORE.add_amount(symbol, amount)

    return JSONResponse(status_code=201, content={"message": f"{amount} units of stock {symbol} were added to your stock record"})