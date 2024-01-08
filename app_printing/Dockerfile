FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_printing

# Установка зависимостей проекта
COPY ./app_printing/requirements.txt /app_printing/
RUN pip install --no-cache-dir --upgrade -r /app_printing/requirements.txt

# Перенос проекта в образ
COPY ./app_printing/app /app_printing/app
COPY .env /app_printing

# Копирование файлов alembic
COPY ./app_printing/migration /app_printing/migration
COPY ./app_printing/alembic.ini /app_printing/alembic.ini

EXPOSE 81

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 158.160.14.173 --port 81"]