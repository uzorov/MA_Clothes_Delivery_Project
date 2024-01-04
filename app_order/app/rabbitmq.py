import json
from uuid import UUID
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message
from app.settings import settings
from app.services.order_service import OrderService  # Импортируем ваш сервис управления задачами
from app.repositories.bd_order_repo import OrderRepo
import logging

logging.basicConfig(level=logging.INFO)

async def process_discount(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        logging.info(data)
        id = UUID(data['id'])
        discount = data['discount']
        order_service = OrderService(OrderRepo())
        order_service.set_discount(id, discount)
    except:
        traceback.print_exc()
        await msg.ack()

async def process_paid_order(msg: IncomingMessage):
    print(str(msg))
    try:
        data = json.loads(msg.body.decode())
        order_id = data['order_id']
        order_service = OrderService(OrderRepo())
        order_service.paid_order(order_id)
    except:
        await msg.ack()

async def consume_tasks(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('process_discount_queue', durable=True)
    paid_order_queue = await channel.declare_queue('payment_queue', durable=True)
    await paid_order_queue.consume(process_paid_order)
    await task_created_queue.consume(process_discount)
    print('Started RabbitMQ consuming...')

    return connection


