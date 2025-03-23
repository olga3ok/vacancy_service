import aiohttp
import certifi
import ssl

from app.core.config import settings
from app.schemas.vacancy import VacancyCreate


class HHParser:
    """
    Класс для работы с API hh.ru
    """
    def __init__(self):
        self.session = None
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=self.connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        self.session = None

    async def get_vacancy(self, vacancy_id: str) -> VacancyCreate:
        """
        Получение данных о вакансии с hh.ru по ID
        """
        if not self.session:
            raise RuntimeError("Session is not initialized.")

        async with self.session.get(f"{settings.HH_API_URL}{vacancy_id}") as response:
            if response.status == 200:
                data = await response.json()

                published_at = data.get("published_at")
                if published_at == "":
                    published_at = None

                # Извлечение данных из ответа API hh.ru
                return VacancyCreate(
                    title=data.get("name", ""),
                    company_name=data.get("employer", {}).get("name", ""),
                    company_address=data.get("address", {}).get("raw", "") if data.get("address") else "",
                    company_logo=data.get("employer", {}).get("logo_urls", {}).get("original", "") \
                        if data.get("employer", {}).get("logo_urls") else "",
                    description=data.get("description", ""),
                    status="active",
                    hh_id=str(data.get("id", "")),
                    published_at=published_at
                )
            else:
                raise Exception(f"Failed to fetch vacancy from HH.ru. Status: {response.status}")

    @classmethod
    async def get_vacancy_from_hh(cls, vacancy_id: str) -> VacancyCreate:
        """
        Статический метод для использования без контекстного менеджера
        Временная сессия для одного запроса
        """
        parser = cls()
        await parser.__aenter__()
        try:
            return await parser.get_vacancy(vacancy_id)
        finally:
            await parser.__aexit__(None, None, None)
