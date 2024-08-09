from fastapi import APIRouter

# Две длинных строчки импортов заменяем на одну короткую.
from app.api.endpoints import meeting_room_router, reservation_router

main_router = APIRouter()
main_router.include_router(
    meeting_room_router, prefix='/meeting_rooms', tags=['Meeting Rooms']
)
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)
