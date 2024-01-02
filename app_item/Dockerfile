FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_item

# Установка зависимостей проекта
COPY ./app_item/requirements.txt /app_item/
RUN pip install --no-cache-dir --upgrade -r /app_item/requirements.txt

# Перенос проекта в образ
COPY ./app_item/app /app_item/app
COPY .env /app_item

# Копирование файлов alembic
COPY ./app_item/migration /app_item/migration
COPY ./app_item/alembic.ini /app_item/alembic.ini

EXPOSE 83

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 83"]