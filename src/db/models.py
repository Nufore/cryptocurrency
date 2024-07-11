from datetime import datetime
from sqlalchemy import Text, BigInteger, DateTime, String, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

DB_USER = 'admin'
DB_PASS = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'cc_db'


engine = create_async_engine(url=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    currency: Mapped[str] = mapped_column(String(5))
    threshold_min: Mapped[float] = mapped_column(Float)
    threshold_max: Mapped[float] = mapped_column(Float)
    is_done: Mapped[bool] = mapped_column(Boolean)
    tg_user_id = mapped_column(BigInteger)

    user: Mapped[int] = mapped_column(ForeignKey("users.id"))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
