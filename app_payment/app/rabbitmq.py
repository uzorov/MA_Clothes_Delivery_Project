import json
import traceback
from asyncio import AbstractEventLoop
from uuid import UUID

from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message

from app.settings import settings
from app.services.payment_service import PaymentService  # Импортируем ваш сервис управления задачами
from app.repositories.payment_repo import PaymentRepo  # Импортируем ваш репозиторий для задач


async def process_payment(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        await send_payment_message(data)
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def process_discount(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        PaymentService(PaymentRepo()).update_payment(data['order_id'], data['sum'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def send_payment_message(id: UUID):
    print('SENDING PAYMENT RESULT')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()
    message_body = json.dumps({'order_id': str(id)})
    print(str(message_body))
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='payment_queue'
    )
    await channel.close()
    await connection.close()

async def send_payment_message_to_printing(id: UUID):
    print('SENDING PAYMENT RESULT')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()
    message_body = json.dumps({'order_id': str(id)})
    print(str(message_body))
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='printing_payment_queue'
    )
    await channel.close()
    await connection.close()

async def consume_payment(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    discount_queue = await channel.declare_queue('discount_queue', durable=True)
    await discount_queue.consume(process_discount)
    task_created_queue = await channel.declare_queue('payment_queue', durable=True)
    await task_created_queue.consume(process_payment)
    printing_queue = await channel.declare_queue('printing_payment_queue', durable=True)
    await printing_queue.consume(process_payment)
    print('Started RabbitMQ consuming for Payment Management...')

    return connection
