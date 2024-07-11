from currency_getter.get_currency import get_exchange_rate_relative_to_usd
from db.models import async_session, Request
from sqlalchemy import select
from bot.starter import bot


async def update_data_and_send_message():
    some_int = 1
    data_dict = await get_exchange_rate_relative_to_usd()
    if not data_dict:
        return
    async with async_session() as session:
        for key, value in data_dict.items():
            print(key)
            print(value)
            stmt = select(Request).where(Request.is_done.is_(False), Request.currency == key)
            data = await session.scalars(stmt)
            requests = data.all()
            for request in requests:
                if value < request.threshold_min:
                    print(request.tg_user_id)
                    await bot.send_message(
                        chat_id=request.tg_user_id,
                        text=f"value rating {value} of {key} is lower than threshold_min {request.threshold_min}"
                    )
                    request.is_done = True
                    session.add(request)
                elif value > request.threshold_max:
                    print(request.tg_user_id)
                    await bot.send_message(
                        chat_id=request.tg_user_id,
                        text=f"value rating {value} of {key} is bigger than threshold_max {request.threshold_max}"
                    )
                    request.is_done = True
                    session.add(request)
            await session.commit()
