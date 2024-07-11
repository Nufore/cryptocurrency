import asyncio
import aiohttp
import json

API_KEY = "2d9628db-8b5f-4546-bcf5-28dccb6bf80f"


async def get_data(symbol: str):
    # Да, нужно вынести все в конфиги, но нет времени
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    async with aiohttp.ClientSession() as session:
        session.headers.update(headers)
        async with session.get(url, params=parameters) as response:
            res = await response.text()
            data = json.loads(res)
            if data["status"]["error_code"] != 0:
                return None
            return data["data"][symbol.upper()]["quote"]["USD"]["price"]
