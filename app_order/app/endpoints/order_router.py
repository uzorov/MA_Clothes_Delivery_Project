from uuid import UUID
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.order_service import OrderService
from app.models.order import Order
import prometheus_client
from fastapi import Response
import app.endpoints.auth_router as auth
from starlette.responses import RedirectResponse
from app.endpoints.auth_router import get_user_role
import logging
from starlette.requests import Request

logging.basicConfig()


host_ip = "192.168.1.92"


order_router = APIRouter(prefix='/order', tags=['Order'])
metrics_router = APIRouter(tags=['Metrics'])

get_orders_count = prometheus_client.Counter(
    "get_orders_count",
    "Number of get requests"
)

get_order_by_id_count = prometheus_client.Counter(
    "get_order_by_id",
    "Number of get requests"
)

create_order_count = prometheus_client.Counter(
    "create_order_count",
    "Number of get requests"
)

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )

@order_router.get('/')
def get_user_orders(request: Request, order_service: OrderService = Depends(OrderService), user: dict = Depends(get_user_role)) -> list[Order]:
    if user['role'] != '':
        if user['role'] == "Viewer" or user['role'] == "Customer":
            get_orders_count.inc(1)
            return order_service.get_user_orders(UUID(user['id']))        
        raise HTTPException(status_code=403, detail=f"{user['role']}")
    else:
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://{host_ip}:80/auth/login")
        
    
        
@order_router.get('/{id}}')
def get_order_by_id(id: UUID, request: Request, order_service: OrderService = Depends(OrderService), user_role: str = Depends(get_user_role)) -> Order:
    try:
        if user_role is not None:
            if user_role == "Viewer" or user_role == "Customer":
                get_order_by_id_count.inc(1)
                return order_service.get_order_by_id(id)
        else:
            return RedirectResponse(url=f"http://{host_ip}:80/auth/login")      
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    
@order_router.post('/')
def create_order(cart: UUID, price: float, order_service: OrderService = Depends(OrderService), user_role: str = Depends(get_user_role)) -> Order:
    try:
        if user_role is not None:
            if user_role == "Viewer" or user_role == "Customer":
                create_order_count.inc(1)
                order = order_service.create_order(cart, price)
                return order.dict()
        else:
            return RedirectResponse(url=f"http://{host_ip}:80/auth/login")        
    except KeyError:
        raise HTTPException(404, f'Order with not found')


@order_router.post('/{id}/paid')
def paid_order(id: UUID, order_service: OrderService = Depends(OrderService), user_role: str = Depends(get_user_role)) -> Order:
    try:
        if user_role is not None:
            if user_role == "Viewer" or user_role == "Customer":
                order = order_service.paid_order(id)
                return order.dict()
        else:
            return RedirectResponse(url=f"http://{host_ip}:80/auth/login")
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be paid')
    
@order_router.post('/{id}/finish')
def finish_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    try:
        order = order_service.finish_order(id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be finished')
