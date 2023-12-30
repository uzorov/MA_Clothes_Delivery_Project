from fastapi import APIRouter, Depends, HTTPException, Header
from uuid import UUID

from app.models.create_payment_request import CreatePaymentRequest
from app.services.payment_service import PaymentService
from app.models.payment_model import Payment, PaymentType


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
    resource=Resource.create({SERVICE_NAME: "payment-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Payment Service'
tracer = trace.get_tracer(name)

payment_router = APIRouter(prefix='/payments', tags=['Payments'])


@payment_router.get('/')
def get_all_payments(payment_service: PaymentService = Depends(PaymentService)) -> list[Payment]:
    with tracer.start_as_current_span("Get payments"):
        return payment_service.get_all_payments()

@payment_router.get('/')
def get_users_payments(payment_service: PaymentService = Depends(PaymentService),
                     user: str = Header(...)) -> list[Payment]:
    with tracer.start_as_current_span("Get payments"):
        user = eval(user)
        try:
            if user['id'] is not None:
                if user['role'] == "Viewer" or user['role'] == "Customer":
                    return payment_service.get_users_payments(user['id'])
        except KeyError:
            raise HTTPException(404, f'Order with id={id} not found')

@payment_router.post('/')
def create_payment(
        payment_info: CreatePaymentRequest,
        user_id: UUID,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    with tracer.start_as_current_span("Create payment"):
        try:
            payment = payment_service.create_payment(payment_info.receiver, payment_info.sum,
                                                     PaymentType(payment_info.type), user_id)
            return payment.dict()
        except KeyError:
            raise HTTPException(400, f'Payment with id={payment_info.id} already exists')


@payment_router.put('/{id}/process')
def process_payment(
        id: UUID,
        payment_service: PaymentService = Depends(PaymentService)
) -> str:
    try:
        result = payment_service.process_payment(id)
        return result
    except KeyError:
        raise HTTPException(404, f'Payment with id={id} not found')


@payment_router.get('/{id}')
def get_payment_by_id(
        id: UUID,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    try:
        payment = payment_service.get_payment_by_id(id)
        return payment.dict()
    except KeyError:
        raise HTTPException(404, f'Payment with id={id} not found')
