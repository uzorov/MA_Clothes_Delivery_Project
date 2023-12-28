FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_delivery

# Установка зависимостей проекта
COPY ./requirements.txt /app_delivery/
RUN pip install --no-cache-dir --upgrade -r /app_delivery/requirements.txt

# Перенос проекта в образ
COPY ./app /app_delivery/app

# Копирование файлов alembic
COPY ./migration /app_delivery/migration
COPY ./alembic.ini /app_delivery/alembic.ini

EXPOSE 80

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 80"]

