import json
from aio_pika import Message, connect_robust
from app.settings import settings
from sqlalchemy.dialects.postgresql import UUID
import asyncio

main_id: UUID


async def get_id(id: UUID):
    global main_id
    main_id = id


async def main(id: UUID):
    print('SENDING UPDATE')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()

    message_body = json.dumps({'id': str(id)})  # Преобразуйте UUID в строку
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='finished_printing_queue'
    )
    # Close the channel and connection
    await channel.close()
    await connection.close()


def run_main(id: UUID):
    asyncio.run(main(id))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_id(main_id))
    run_main(main_id)
