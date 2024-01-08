from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.order_service import OrderService
from app.models.order import Order, CreateOrderRequest
import prometheus_client
from fastapi import Response
import logging
from starlette.requests import Request
import httpx
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace import Span, StatusCode
from opentelemetry import context
from app.settings import settings

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "order-service"})
    )
)
jaeger_exporter = JaegerExporter(
    # !!!!!!Нужно поменять значение в .env
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'Order Service'
tracer = trace.get_tracer(name)

logging.basicConfig()

logging.basicConfig()

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


# Function to get current span
def get_current_span() -> Span:
    current_span = context.get_value().get(Span, None)
    if current_span is None:
        return trace.DefaultSpan()
    return current_span


# Function to add endpoint information to the current span
def add_endpoint_info(span: Span, endpoint_name: str) -> None:
    span.set_attribute("http.route", endpoint_name)


# Function to add operation result to the current span
def add_operation_result(span: Span, result: str) -> None:
    span.set_attribute("custom.result", result)


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )


payment_service_url = "https://bbagsn9ksci9tifcinu9.containers.yandexcloud.net"
printing_service_url = "https://bbaif5o8621h44fjp96q.containers.yandexcloud.net"


def user_staff_admin(role):
    if role == "client" or role == "staff" or role == "admin":
        return True
    return False

def staff_admin(role):
    if role == "staff" or role == "admin":
        return True
    return False


def make_request_to_payment_service(data):
    print("Payment req")
    data = {'sum': str(data['price']), 'order_id': str(data['id']), 'user_id': str(data['user_id'])}
    url = f"{payment_service_url}/api/payments/"
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request to payment: {response.status_code}, {response.text}")


def make_request_to_printing_service(data):
    print("Printing req")
    url = f"{printing_service_url}/api/printing/"
    data = {'id': str(data['id'])}
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request to payment: {response.status_code}, {response.text}")


@order_router.get('/')
def get_user_orders(request: Request, order_service: OrderService = Depends(OrderService),
                    user: str = Header(...), ) -> None:
    with tracer.start_as_current_span("Get user orders") as span:
        add_endpoint_info(span, "/")
        user = eval(user)
        if user['id'] is not None:
            if user_staff_admin(user['role']):
                add_operation_result(span, "success")
                get_orders_count.inc(1)
                return order_service.get_user_orders(UUID(user['id']))
            add_operation_result(span, "failure")
            raise HTTPException(status_code=403, detail=f"{user['role']}")


@order_router.get('/{id}')
def get_order_by_id(id: UUID, request: Request, order_service: OrderService = Depends(OrderService),
                    user: str = Header(...), ) -> Order:
    user = eval(user)
    with tracer.start_as_current_span("Get order by id") as span:
        add_endpoint_info(span, "/{id}")
        try:
            if user['id'] is not None:
                if user_staff_admin(user['role']):
                    get_order_by_id_count.inc(1)
                    add_operation_result(span, "success")
                    return order_service.get_user_order_by_id(id, user['id'])
                raise HTTPException(403)
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'Order with id={id} not found')


@order_router.post('/')
def create_order(order_info: CreateOrderRequest, order_service: OrderService = Depends(OrderService)) -> Order:
    print("___________CREATE_ORDER___________________")
    with tracer.start_as_current_span("Create order") as span:
        add_endpoint_info(span, "/")
        try:
            create_order_count.inc(1)
            order = order_service.create_order(order_info.cart, order_info.price, order_info.user_id)
            print("Added to db")
            make_request_to_printing_service(order.dict())
            make_request_to_payment_service(order.dict())
            add_operation_result(span, "success")
            return order.dict()
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'Order with not found')


@order_router.post('/{id}/paid')
def paid_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    with tracer.start_as_current_span("Paid order") as span:
        add_endpoint_info(span, "/{id}/paid")
        try:
            order = order_service.paid_order(id)
            add_operation_result(span, "success")
            return order.dict()
        except KeyError:
            add_operation_result(span, f'Order with id={id} not found')
            raise HTTPException(404, f'Order with id={id} not found')
        except ValueError:
            add_operation_result(span, f'Order with id={id} can\'t be paid')
            raise HTTPException(400, f'Order with id={id} can\'t be paid')


@order_router.post('/{id}/finish')
def finish_order(id: UUID, order_service: OrderService = Depends(OrderService)) -> Order:
    with tracer.start_as_current_span("Finish order") as span:
        add_endpoint_info(span, "/{id}/finish")
        try:
            order = order_service.finish_order(id)
            add_operation_result(span, "success")
            return order.dict()
        except KeyError:
            add_operation_result(span, f'Order with id={id} not found')
            raise HTTPException(404, f'Order with id={id} not found')
        except ValueError:
            add_operation_result(span, f'Order with id={id} can\'t be finished')
            raise HTTPException(400, f'Order with id={id} can\'t be finished')
