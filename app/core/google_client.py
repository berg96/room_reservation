import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
# Подключаем настройки
from app.core.config import settings
# Список разрешений
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

with open(settings.service_account_file, 'r') as file:
    service_account_info = json.load(file)
# Получаем объект учётных данных
cred = ServiceAccountCreds(scopes=SCOPES, **service_account_info)


# Создаём экземпляр класса Aiogoogle
async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
