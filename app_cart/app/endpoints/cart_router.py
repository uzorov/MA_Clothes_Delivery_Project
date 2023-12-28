from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from app.services.cart_service import CartService
from app.models.cart import Cart, Item
import prometheus_client
from fastapi import Response
import app.endpoints.auth_router as auth
from starlette.responses import RedirectResponse
from app.endpoints.auth_router import get_user_role


cart_router = APIRouter(prefix='/cart', tags=['Cart'])
metrics_router = APIRouter(tags=['Metrics'])

get_orders_count = prometheus_client.Counter(
    "get_cart_count",
    "Number of get requests"
)

get_order_by_id_count = prometheus_client.Counter(
    "get_cart_by_id_count",
    "Number of get requests"
)

create_order_count = prometheus_client.Counter(
    "create_cart_count",
    "Number of get requests"
)

host_ip = "172.19.64.1"

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )

@cart_router.get('/test')
def get_carts_test(cart_service: CartService = Depends(CartService)) -> list[Cart]:
    return cart_service.get_carts()

@cart_router.get('/')
def get_carts(cart_service: CartService = Depends(CartService), user_role: str = Depends(get_user_role)) -> list[Cart]:
    if user_role is not None:
        if user_role == "Viewer" or user_role == "Customer":
            get_cart_count.inc(1)
            return cart_service.get_carts()
        raise HTTPException(status_code=403, detail=f"{user_role}")
    else:
        return RedirectResponse(url=f"http://{host_ip}:80/auth/login")

@cart_router.get('/{id}}')
def get_cart_by_id(id: UUID, cart_service: CartService = Depends(CartService), user_role: str = Depends(get_user_role)) -> Cart:
    try:
        if user_role is not None:
            if user_role == "Viewer" or user_role == "Customer":
                get_cart_by_id_count.inc(1)
                return cart_service.get_cart_by_id(id)
        else:
            return RedirectResponse(url=f"http://{host_ip}:80/auth/login")
    except KeyError:
        raise HTTPException(404, f'Cart with id={id} not found')

@cart_router.post('/')
def create_or_update_cart(item: Item, cart_service: CartService = Depends(CartService), id: Optional[UUID] = None, user_role: str = Depends(get_user_role)) -> Cart:
    try:
        if user_role is not None:
            if user_role == "Viewer" or user_role == "Customer":
                if id and cart_service.get_cart_by_id(id):
                    create_cart_count.inc(1)
                    order = cart_service.update_cart(id, item)
                    return order.__dict__
                order = cart_service.create_cart(item)
                return order.dict()
        else:
            return RedirectResponse(url=f"http://{host_ip}:80/auth/login")  
    except KeyError:
        raise HTTPException(404, f'Order with {id} not found')
