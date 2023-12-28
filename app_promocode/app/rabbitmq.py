import json
from uuid import UUID
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message
from app.settings import settings
from app.services.promocode_service import PromocodeService  # Импортируем ваш сервис управления задачами
from app.repo.local_promocode_repo import PromocodeRepo 
import logging

logging.basicConfig(level=logging.INFO)


async def process_promocode(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        await send_discount(data['discount'], data['id'])
    except:
        await msg.ack()

async def send_discount(discount: float, id: UUID):
    print('Sending code')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()
    message_body = json.dumps({'discount': discount, 'id': str(id)})
    logging.info(message_body, 'rab_prom')
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='process_discount_queue'
    )
    await channel.close()
    await connection.close()

async def consume_tasks(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('process_promocode_queue', durable=True)


    await task_created_queue.consume(process_promocode)
    print('Started RabbitMQ consuming for Task Management...')

    return connection