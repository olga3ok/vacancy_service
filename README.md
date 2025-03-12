# Vacancy Sevice
Сервис предоставляет HTTP API и веб-интерфейс для работы с вакансиями, получаемыми с портала hh.ru. Сервис позволяет создавать, просматривать, обновлять и удалять информацию о вакансиях.
- REST API для работы с вакансиями
- Авторизация пользователей через JWT (Bearer)
- Веб-интерфейс на React
- Парсинг и сохранение данных из API hh.ru
- Контейнеризация с помощью Docker

## Стек технологий
#### Backend: 
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- aiohttp
- JWT для авторизации

#### Frontend:
- React 19
- Axios
- Tabler UI

## API Endpoints
##### Вакансии
```
POST /api/v1/vacancy/create - Создание вакансии
PUT/PATCH /api/v1/vacancy/update - Обновление вакансии
GET /api/v1/vacancy/get/<id> - Получение вакансии
DELETE /api/v1/vacancy/delete/<id> - Удаление вакансии
```
##### Авторизация
```
POST /token - Получение JWT токена
```
## Запуск проекта (Docker)
1. Клонируйте репозиторий:
```
git clone git@github.com:olga3ok/vacancy_service.git
cd vacancy-service
```
2. Создайте файл backend/.env:
```
SECRET_KEY=
DATABASE_URL=sqlite:///./app.db
HH_API_URL=https://api.hh.ru/vacancies/
DEFAULT_USERNAME=
DEFAULT_PASSWORD=
```
3. Запустите проект с помощью Docker Compose
```
docker-compose up -d
```
Создать пользователя можно при помощи скрипта backend/app/utils/add_user.py

Сгенерировать секретный ключ - backend/app/utils/secretkey_gen.py

### Примеры запросов к API:
1. Получение токена:
```
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ваш_логин&password=ваш_пароль"
```
2. Получение информации о вакансии:
```
curl -X GET http://localhost:8000/api/v1/vacancy/get/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```
