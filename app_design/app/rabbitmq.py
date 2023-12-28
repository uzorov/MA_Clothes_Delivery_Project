import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message

from app.settings import settings
from app.services.design_service import DesignService  # Импортируем ваш сервис управления задачами
from app.repositories.design_repo import DesignRepo  # Импортируем ваш репозиторий для задач

async def process_design(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        await send_design_message(data)
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def send_design_message(data: str):
    print('SENDING DESIGN')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()


    message_body = json.dumps(data)
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='design_queue'
    )
    # Close the channel and connection
    await channel.close()
    await connection.close()



async def consume_design(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('design_queue', durable=True)

    await task_created_queue.consume(process_design)
    print('Started RabbitMQ consuming for Design Management...')

    return connection

