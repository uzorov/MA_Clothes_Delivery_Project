import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message

from app.settings import settings
from app.services.payment_service import PaymentService  # Импортируем ваш сервис управления задачами
from app.repositories.payment_repo import PaymentRepo  # Импортируем ваш репозиторий для задач


# async def process_payment(msg: IncomingMessage):
#     try:
#         data = json.loads(msg.body.decode())
#         await send_payment_message(data)
#     except:
#         traceback.print_exc()
#     finally:
#         await msg.ack()


async def send_payment_message(data: str):
    print('SENDING PAYMENT RESULT')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()
    print(data)
    message_body = json.dumps(data)
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='payment_queue'
    )
    await channel.close()
    await connection.close()


# async def consume_design(loop: AbstractEventLoop) -> AbstractRobustConnection:
#     connection = await connect_robust(settings.amqp_url, loop=loop)
#     channel = await connection.channel()
#
#     task_created_queue = await channel.declare_queue('payment_queue', durable=True)
#
#     await task_created_queue.consume(process_payment)
#     print('Started RabbitMQ consuming for Payment Management...')
#
#     return connection
