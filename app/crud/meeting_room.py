# Импортируем sessionmaker из файла с настройками БД.
from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


# Функция работает с асинхронной сессией,
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate
) -> MeetingRoom:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_room_data = new_room.dict()

    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    db_room = MeetingRoom(**new_room_data)

    # Создаём асинхронную сессию через контекстный менеджер.
    async with AsyncSessionLocal() as session:
        # Добавляем созданный объект в сессию.
        # Никакие действия с базой пока ещё не выполняются.
        session.add(db_room)

        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        await session.commit()

        # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
        await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room


# Добавляем новую асинхронную функцию.
async def get_room_id_by_name(room_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        # Получаем объект класса Result.
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        # Извлекаем из него конкретное значение.
        db_room_id = db_room_id.scalars().first()
    return db_room_id
