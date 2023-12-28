from fastapi import FastAPI
from fastapi import FastAPI
import asyncio
from app import rabbitmq
from app.endpoints.promocode_router import promocode_router

app = FastAPI(title='Promocode Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume_tasks(loop))


app.include_router(promocode_router, prefix='/api')
