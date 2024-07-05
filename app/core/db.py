# Все классы и функции для асинхронной работы
# находятся в модуле sqlalchemy.ext.asyncio.
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
