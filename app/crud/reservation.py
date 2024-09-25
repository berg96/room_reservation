from datetime import datetime
from typing import Optional

from sqlalchemy import select, or_, and_, between, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate
]):
    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        # Выполняем запрос.
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
        self,
        room_id: int,
        session: AsyncSession,
    ):
        return (
            await session.execute(select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            ))
        ).scalars().all()

    async def get_by_user(
        self,
        user: int,
        session: AsyncSession,
    ):
        return (
            await session.execute(select(Reservation).where(
                Reservation.user_id == user.id
            ))
        ).scalars().all()

    async def get_count_res_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            # Получаем количество бронирований переговорок за период
            select([
                Reservation.meetingroom_id,
                func.count(Reservation.meetingroom_id)
            ]).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        reservations = reservations.all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
