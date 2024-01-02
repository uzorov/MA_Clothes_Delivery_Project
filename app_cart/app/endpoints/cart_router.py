from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from typing import Optional
from app.services.cart_service import CartService
from app.models.cart import Cart, Item
import prometheus_client
from fastapi import Response
import app.endpoints.auth_router as auth
from starlette.responses import RedirectResponse
from app.endpoints.auth_router import get_user_role

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "cart-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Cart Service'
tracer = trace.get_tracer(name)

cart_router = APIRouter(prefix='/cart', tags=['Cart'])
metrics_router = APIRouter(tags=['Metrics'])

get_cart_count = prometheus_client.Counter(
    "get_cart_count",
    "Number of get requests"
)

get_cart_by_id_count = prometheus_client.Counter(
    "get_cart_by_id_count",
    "Number of get requests"
)

create_cart_count = prometheus_client.Counter(
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

@cart_router.get('/')
def get_carts(cart_service: CartService = Depends(CartService)) -> list[Cart]:
    with tracer.start_as_current_span("Get carts"):
        get_cart_count.inc(1)
        return cart_service.get_carts()

@cart_router.get('/{id}}')
def get_cart_by_id(id: UUID, cart_service: CartService = Depends(CartService), user: str = Header(...)) -> Cart:
    with tracer.start_as_current_span("Get cart by id"):
        user = eval(user)
        try:
            if user['id'] is not None:
                if user['role'] == "Viewer" or user['role'] == "Customer":
                    get_cart_by_id_count.inc(1)
                    return cart_service.get_cart_by_user(id, user['id'])
        except KeyError:
            raise HTTPException(404, f'Cart with id={id} not found')

@cart_router.post('/')
def create_or_update_cart(item: Item, cart_service: CartService = Depends(CartService), user: str = Header(...)) -> Cart:
    user = eval(user)
    try:
        if user['id'] is not None:
            if user['role'] == "Viewer" or user['role'] == "Customer":
                if cart_service.get_cart_by_user(user['id']):
                    create_cart_count.inc(1)
                    order = cart_service.update_cart(user['id'], item)
                    return order.__dict__
                order = cart_service.create_cart(item, user['id'])
                return order.dict()  
    except KeyError:
        raise HTTPException(404, f'Order with {id} not found')

