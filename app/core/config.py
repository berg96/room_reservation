from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = (
        'Приложение предоставляет возможность бронировать '
        'помещения на определённый период времени'
    )
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
