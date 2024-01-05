from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.endpoints.cart_router import cart_router, metrics_router

app = FastAPI(title='Cart Service')

app.include_router(cart_router, prefix='/api')
app.add_middleware(SessionMiddleware, secret_key='karaseva1234')
app.include_router(metrics_router)
