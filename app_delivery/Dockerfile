FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_delivery

# Установка зависимостей проекта
COPY ./app_delivery/requirements.txt /app_delivery/
RUN pip install --no-cache-dir --upgrade -r /app_delivery/requirements.txt

# Перенос проекта в образ
COPY ./app_delivery/app /app_delivery/app
COPY .env /app_delivery

# Копирование файлов alembic
COPY ./app_delivery/migration /app_delivery/migration
COPY ./app_delivery/alembic.ini /app_delivery/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 158.160.14.173 --port 80"]

