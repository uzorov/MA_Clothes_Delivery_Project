import asyncio

from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.payment_router import payment_router

app = FastAPI(title='Payment Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    # asyncio.ensure_future(rabbitmq.consume_tasks(loop))


app.include_router(payment_router, prefix='/api')
