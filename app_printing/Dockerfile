FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_printing

# Установка зависимостей проекта
COPY ./requirements.txt /app_printing/
RUN pip install --no-cache-dir --upgrade -r /app_printing/requirements.txt

# Перенос проекта в образ
COPY ./app /app_printing/app

# Копирование файлов alembic
COPY ./migration /app_printing/migration
COPY ./alembic.ini /app_printing/alembic.ini

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 81"]