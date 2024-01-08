FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_cart

# Установка зависимостей проекта
COPY ./app_cart/requirements.txt /app_cart/
RUN pip install --no-cache-dir --upgrade -r /app_cart/requirements.txt

# Перенос проекта в образ
COPY ./app_cart/app /app_cart/app
COPY .env /app_cart

# Копирование файлов alembic
COPY ./app_cart/migration /app_cart/migration
COPY ./app_cart/alembic.ini /app_cart/alembic.ini

EXPOSE 86

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 158.160.14.173 --port 86"]
