# /app/main.py

import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.delivery_router import delivery_router, metrics_router
import logging
from logging_loki import LokiHandler

app = FastAPI(title='Delivery Service')

loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)
logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(delivery_router, prefix='/api')
app.include_router(metrics_router)
