import asyncio

from fastapi import FastAPI
from app import rabbitmq
from app.endpoints.item_router import item_router

app = FastAPI(title='Item Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    # asyncio.ensure_future(rabbitmq.consume_tasks(loop))


app.include_router(item_router, prefix='/api')
