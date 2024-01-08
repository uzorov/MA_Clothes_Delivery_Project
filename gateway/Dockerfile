FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /gateway

# Перенос проекта в образ
COPY ./gateway/app /gateway/app

EXPOSE 87

CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
