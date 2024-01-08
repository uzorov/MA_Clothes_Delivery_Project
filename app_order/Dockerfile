FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_order

# Установка зависимостей проекта
COPY ./app_order/requirements.txt /app_order/
RUN pip install --no-cache-dir --upgrade -r /app_order/requirements.txt

# Перенос проекта в образ
COPY ./app_order/app /app_order/app
COPY .env /app_order

# Копирование файлов alembic
COPY ./app_order/migration /app_order/migration
COPY ./app_order/alembic.ini /app_order/alembic.ini

EXPOSE 84

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 158.160.14.173 --port 84"]