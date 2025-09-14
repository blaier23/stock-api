import httpx
from bs4 import BeautifulSoup
from typing import Dict

BASE_URL = "https://www.marketwatch.com/investing/stock"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

async def fetch_marketwatch_performance(symbol: str) -> Dict[str, str]:
    """Scrape MarketWatch performance section for stock."""
    url = f"{BASE_URL}/{symbol.lower()}"
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError(f"Marketwatch error {response.status_code}: {response.text[:200]}")

    soup = BeautifulSoup(response.text, "html.parser")

    performance = {}
    
    perf_section = soup.find("div", {"class": "element element--table performance"})
    if perf_section:
        table = perf_section.find("table")
        if table:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    performance[key] = val

    return performance