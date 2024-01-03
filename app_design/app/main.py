# import asyncio
#
# from fastapi import FastAPI
#
# from app import rabbitmq
# from app.endpoints.design_router import design_router
#
# app = FastAPI(title='Design Service')
#
#
# @app.on_event('startup')
# def startup():
#     loop = asyncio.get_event_loop()
#     # asyncio.ensure_future(rabbitmq.consume_tasks(loop))
#
#
# app.include_router(design_router, prefix='/api')
