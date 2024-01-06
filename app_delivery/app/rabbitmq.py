# /app/rabbitmq.py

import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message

from app.settings import settings
from app.services.delivery_service import DeliveryService
from app.repositories.db_delivery_repo import DeliveryRepo
from uuid import UUID


async def process_finished_printing(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        DeliveryService(DeliveryRepo()).create_delivery(data['id'])
    except:
        traceback.print_exc()
        await msg.ack()

# send_finish_delivery
async def send_finish_delivery(id: UUID):
    print('Sending code')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()
    message_body = json.dumps({'id': str(id)})
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='process_finish_delivery_queue'
    )
    await channel.close()
    await connection.close()

async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    finished_printing_queue = await channel.declare_queue('finished_printing_queue', durable=True)
    await finished_printing_queue.consume(process_finished_printing)
    finish_delivery_queue = await channel.declare_queue('finish_delivery_queue', durable=True)
    await finish_delivery_queue.consume(send_finish_delivery)
    print('Started RabbitMQ consuming...')

    return connection
