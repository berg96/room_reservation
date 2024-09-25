from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = (
        'Приложение предоставляет возможность бронировать '
        'помещения на определённый период времени'
    )
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    service_account_file: Optional[str] = None
    email_user: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
