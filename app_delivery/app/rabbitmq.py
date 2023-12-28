# /app/rabbitmq.py

import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.delivery_service import DeliveryService
from app.repositories.db_delivery_repo import DeliveryRepo


async def process_finished_printing(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DeliveryService(DeliveryRepo()).create_delivery(data['id'])
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    finished_printing_queue = await channel.declare_queue('finished_printing_queue', durable=True)
    await finished_printing_queue.consume(process_finished_printing)

    print('Started RabbitMQ consuming...')

    return connection
