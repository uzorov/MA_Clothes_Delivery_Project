from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.cart_service import CartService
from app.models.cart import Cart, Item
import prometheus_client
from fastapi import Response
import httpx


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

target_service_url = "http://app_order:84"

def make_request_to_target_service(data):
    print("_________________MAKE REQ__________________")
    print(str(data))
    url = f"{target_service_url}/api/order/"
    json_data = {'user_id': str(data['user_id']),'cart':str(data['cart']),'price':str(data['price'])}
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=json_data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request: {response.status_code}, {response.text}")

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
def get_cart_by_id(cart_service: CartService = Depends(CartService), user: str = Header(...)) -> Cart:
    with tracer.start_as_current_span("Get cart by id"):
        user = eval(user)
        try:
            if user['id'] is not None:
                if user['role'] == "Viewer" or user['role'] == "Customer":
                    get_cart_by_id_count.inc(1)
                    return cart_service.get_cart_by_user(user['id'])
        except KeyError:
            raise HTTPException(404, f'Cart with id={id} not found')

# @cart_router.post('/')
# def create_or_update_cart(item: Item, cart_service: CartService = Depends(CartService), user: str = Header(...)) -> Cart:
#     user = eval(user)
#     try:
#         if user['id'] is not None:
#             if user['role'] == "Viewer" or user['role'] == "Customer":
#                 if cart_service.get_cart_by_user(user['id']):
#                     create_cart_count.inc(1)
#                     cart = cart_service.update_cart(user['id'], item)
#                     return cart.__dict__
#                 cart = cart_service.create_cart(item, user['id'])
#                 return cart.dict()
#     except KeyError:
#         raise HTTPException(404, f'Cart with {id} not found')


# NEXT FUN IS FOR TEST ONLY, IN PROD WE'LL USE FUN ABOVE
@cart_router.post('/')
def create_or_update_cart(item: Item, cart_service: CartService = Depends(CartService)) -> Cart:
    id = "801b87ac-6994-44b4-a65f-3fd7fdf3ca1b"
    try:
        cart = cart_service.create_cart(item, id)
        return cart.dict()
    except KeyError:
        raise HTTPException(404, f'Cart with {id} not found')

# @cart_router.post('/create_order')
# def create_order(cart_service: CartService = Depends(CartService), user: str = Header(...)) -> Cart:
#     user = eval(user)
#     try:
#         if user['id'] is not None:
#             if user['role'] == "Viewer" or user['role'] == "Customer":
#                 cart = cart_service.get_cart_by_user(user['id'])
#                 if cart:
#                     data = {'user_id': user['id'], 'cart': cart.id, 'price': cart.total}
#                     make_request_to_target_service(data)
#                     cart = cart_service.set_cart_status(user['id'])
#                     return cart.__dict__
#     except KeyError:
#         raise HTTPException(404, f'Cart with {id} not found')

@cart_router.post('/create_order')
def create_order(user: UUID, cart_service: CartService = Depends(CartService)) -> Cart:
    try:
        print("Router--------------------------------------------------------")
        print(user)
        cart = cart_service.get_cart_by_user(user)
        data = {'user_id': str(user), 'cart': str(cart.id), 'price': str(cart.total)}
        try:
            make_request_to_target_service(data)
        except KeyError:
            raise HTTPException(404, f'Cart make request')
        cart = cart_service.set_cart_status(user)
        return cart.__dict__
    except KeyError:
        raise HTTPException(404, f'Cart with user {user} not found')