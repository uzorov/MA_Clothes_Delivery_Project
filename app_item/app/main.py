from fastapi import FastAPI
from app.endpoints.item_router import item_router

app = FastAPI(title='Item Service')


app.include_router(item_router)