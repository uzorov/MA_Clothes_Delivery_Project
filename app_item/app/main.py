import asyncio

from fastapi import FastAPI
from app import rabbitmq
from app.endpoints.item_router import item_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Item Service')


origins = [
    "http://our_web_site:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WHITELISTED_IPS = ['http://172.18.0.1']
# @app.middleware('http')
# async def validate_ip(request: Request, call_next):
#     ip = str(request.client.host)
#     if ip not in WHITELISTED_IPS:
#         data = {
#             'message': f'IP {ip} is not allowed to access this resource.'
#         }
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
#     return await call_next(request)

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    # asyncio.ensure_future(rabbitmq.consume_tasks(loop))


app.include_router(item_router, prefix='/api')

