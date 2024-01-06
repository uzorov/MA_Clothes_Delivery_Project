from fastapi import APIRouter, Depends, HTTPException, Header
from uuid import UUID
import asyncio

from app.models.create_payment_request import CreatePaymentRequest
from app.services.payment_service import PaymentService
from app.models.payment_model import Payment
from app.rabbitmq import send_payment_message, send_payment_message_to_printing

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
        resource=Resource.create({SERVICE_NAME: "payment-service"})
    )
)
jaeger_exporter = JaegerExporter(
    # !!!!!!Нужно поменять значение в .env
    agent_host_name=settings.host_ip,
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'Payment Service'

tracer = trace.get_tracer(name)

payment_router = APIRouter(prefix='/payments', tags=['Payments'])


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


@payment_router.get('/')
def get_all_payments(payment_service: PaymentService = Depends(PaymentService)) -> list[Payment]:
    with tracer.start_as_current_span("Get payments") as span:
        add_endpoint_info(span, "/")
        try:
            result = payment_service.get_all_payments()
            add_operation_result(span, "success")
            return result
        except Exception as e:
            add_operation_result(span, "failure")
            raise HTTPException(500, f'Internal Server Error: {str(e)}')


@payment_router.get('/get-user-payments')
def get_users_payments(payment_service: PaymentService = Depends(PaymentService),
                       user: str = Header(...)) -> list[Payment]:
    with tracer.start_as_current_span("Get users payments") as span:
        user = eval(user)
        add_endpoint_info(span, "/get-user-payments")
        try:
            if user['id'] is not None:
                if user['role'] == "Viewer" or user['role'] == "Customer":
                    result = payment_service.get_user_payments(user['id'])
                    add_operation_result(span, "success")
                    return result
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'Order with user {user["id"]} not found')


@payment_router.post('/')
def create_payment(
        payment_info: CreatePaymentRequest,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    with tracer.start_as_current_span("Create payment") as span:
        add_endpoint_info(span, '/ [POST]')
        try:
            print(str(payment_info))

            payment = payment_service.create_payment(payment_info.sum,
                                                     payment_info.user_id, payment_info.order_id)
            print(str(payment))
            add_operation_result(span, "Successful")
            return payment.dict()
        except KeyError:
            add_operation_result(span, f'Payment with id={payment_info.id} already exists')
            raise HTTPException(400, f'Payment with id={payment_info.id} already exists')

@payment_router.post('/update_payment')
def update_payment(
        payment_info: CreatePaymentRequest,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    with tracer.start_as_current_span("Update payment") as span:
        add_endpoint_info(span, "/update_payment/{id}")
        try:
            print("UPDATE PAYMENT:"+str(payment_info))
            payment = payment_service.update_payment(payment_info.order_id, payment_info.sum)
            add_operation_result(span, "success")
            return payment.dict()
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'payment with id={payment_info.id} not found')

@payment_router.post('/{id}/process')
def process_payment(
        id: UUID,
        payment_service: PaymentService = Depends(PaymentService)
) -> str:
    try:
        result = payment_service.process_payment(id)
        if (result == "Payment processed successfully"):
            payment = payment_service.get_payment_by_id(id)
            asyncio.run(send_payment_message(payment.order_id))
            asyncio.run(send_payment_message_to_printing(payment.order_id))

        return result
    except KeyError:
        raise HTTPException(404, f'Payment with id={id} not found')


@payment_router.get('/{id}')
def get_payment_by_id(
        id: UUID,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    with tracer.start_as_current_span("Create payment") as span:
        add_endpoint_info(span, "/{id}")
        try:
            payment = payment_service.get_payment_by_id(id)
            add_operation_result(span, "Successful")
            return payment.dict()
        except KeyError:
            add_operation_result(span, f'Payment with id={id} not found')
            raise HTTPException(404, f'Payment with id={id} not found')
