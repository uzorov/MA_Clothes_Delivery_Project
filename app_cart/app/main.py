from fastapi import FastAPI
from app.endpoints.cart_router import cart_router
from starlette.middleware.sessions import SessionMiddleware
from app.endpoints.cart_router import cart_router, metrics_router
from app.endpoints.auth_router import auth_router

app = FastAPI(title='Cart Service')

app.include_router(cart_router)
app.add_middleware(SessionMiddleware, secret_key='karaseva1234')
app.include_router(metrics_router)
app.include_router(auth_router)
