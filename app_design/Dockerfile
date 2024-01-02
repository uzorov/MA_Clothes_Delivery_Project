# FROM python:3.10
#
# # Выбор папки, в которой будет вестись работа
# WORKDIR /app_design
#
# # Установка зависимостей проекта
# COPY ./app_design/requirements.txt /app_design/
# RUN pip install --no-cache-dir --upgrade -r /app_design/requirements.txt
#
# # Перенос проекта в образ
# COPY ./app_design/app /app_design/app
# COPY .env /app_design
#
# # Копирование файлов alembic
# COPY ./app_design/migration /app_design/migration
# COPY ./app_design/alembic.ini /app_design/alembic.ini
#
# EXPOSE 83
#
# CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 83"]
