# /app_printing/rabbitmq.py
import json
from asyncio import AbstractEventLoop

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection
from app.repositories.db_printing_repo import PrintingRepo
from app.services.printing_service import PrintingService
from app.settings import settings


async def process_paid_order(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        PrintingService(PrintingRepo()).begin_printing(data['id'])
    except:
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    paid_order_queue = await channel.declare_queue('paid_order_queue', durable=True)
    await paid_order_queue.consume(process_paid_order)

    print('Started RabbitMQ consuming...')

    return connection
