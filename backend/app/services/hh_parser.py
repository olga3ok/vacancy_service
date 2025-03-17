import aiohttp
import certifi
import ssl

from app.core.config import settings
from app.schemas.vacancy import VacancyCreate


ssl_context = ssl.create_default_context(cafile=certifi.where())


async def get_vacancy_from_hh(vacancy_id: str) -> VacancyCreate:
    """
    Получение данных о вакансии с hh.ru по ID
    """
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(f"{settings.HH_API_URL}{vacancy_id}") as response:
            if response.status == 200:
                data = await response.json()

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
                    published_at=data.get("published_at", "")
                )
            else:
                raise Exception(f"Failed to fetch vacancy from HH.ru. Status: {response.status}")
