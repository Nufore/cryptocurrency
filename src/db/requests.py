from db.models import async_session
from db.models import User, Request
from sqlalchemy import select


async def get_user_id(tg_id: int):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)
        return user.id


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt)

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_currency_request(currency: str, threshold_min: int, threshold_max: int, tg_user_id):
    user_id = await get_user_id(tg_id=tg_user_id)

    async with async_session() as session:
        session.add(Request(
            currency=currency,
            threshold_min=float(threshold_min),
            threshold_max=float(threshold_max),
            user=user_id,
            tg_user_id=tg_user_id,
            is_done=False,
        ))
        await session.commit()
