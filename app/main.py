from fastapi import FastAPI

from app.api.meeting_room import router
# Импортируем настройки проекта из config.py.
from app.core.config import settings

# Устанавливаем заголовок приложения при помощи аргумента title,
# в качестве значения указываем атрибут app_title объекта settings.
app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(router)
