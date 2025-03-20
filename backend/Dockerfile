# Сборка
FROM python:3.10-slim AS build-stage

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user --upgrade -r requirements.txt

# Запуск
FROM python:3.10-slim AS runtime-stage

WORKDIR /app

COPY --from=build-stage /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]