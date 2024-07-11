from sqlalchemy import select

from src.db.models import async_session
from src.db.models import Request

from src.currency_getter.get_api_data import get_data


async def get_curr_name():
    data_list = []
    async with async_session() as session:
        stmt = select(Request).where(Request.is_done.is_(False))
        data = await session.scalars(stmt)
        requests = data.all()
        for request in requests:
            if request.currency not in data_list:
                data_list.append(request.currency)

    if data_list:
        return data_list


async def get_exchange_rate_relative_to_usd():
    symbols = await get_curr_name()
    if not symbols:
        return None
    currency_price_dict = {}
    for symbol in symbols:
        currency_price_dict[symbol] = await get_data(symbol)

    return currency_price_dict
