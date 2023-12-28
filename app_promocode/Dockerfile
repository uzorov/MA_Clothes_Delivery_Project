FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_promocode

# Установка зависимостей проекта
COPY ./app_promocode/requirements.txt /app_promocode/
RUN pip install --no-cache-dir --upgrade -r /app_promocode/requirements.txt

# Перенос проекта в образ
COPY ./app_promocode/app /app_promocode/app
COPY .env /app_promocode

# Копирование файлов alembic
COPY ./app_promocode/migration /app_promocode/migration
COPY ./app_promocode/alembic.ini /app_promocode/alembic.ini

EXPOSE 85

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 85"]
