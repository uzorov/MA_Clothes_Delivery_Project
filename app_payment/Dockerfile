FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_payment

# Установка зависимостей проекта
COPY ./app_payment/requirements.txt /app_payment/
RUN pip install --no-cache-dir --upgrade -r /app_payment/requirements.txt

# Перенос проекта в образ
COPY ./app_payment/app /app_payment/app
COPY .env /app_payment

# Копирование файлов alembic
COPY ./app_payment/migration /app_payment/migration
COPY ./app_payment/alembic.ini /app_payment/alembic.ini

EXPOSE 82

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 82"]