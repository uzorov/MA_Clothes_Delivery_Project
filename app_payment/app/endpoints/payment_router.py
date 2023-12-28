from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.models.create_payment_request import CreatePaymentRequest
from app.services.payment_service import PaymentService
from app.models.payment_model import Payment, PaymentType

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Команда запуска бобра
# docker run -d --name jaeger -e COLLECTOR_OTLP_ENABLED=true -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14250:14250 -p 14268:14268 -p 14269:14269 -p 4317:4317 -p 4318:4318 -p 9411:9411 jaegertracing/all-in-one:next-release
# opentelemetry-instrument --service_name payment.api uvicorn app.main:app

provider = TracerProvider()

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

payment_router = APIRouter(prefix='/payments', tags=['Payments'])


@payment_router.get('/')
def get_all_payments(payment_service: PaymentService = Depends(PaymentService)) -> list[Payment]:
    with tracer.start_as_current_span("Get payments") as span:
        return payment_service.get_all_payments()


@payment_router.post('/')
def create_payment(
        payment_info: CreatePaymentRequest,
        payment_service: PaymentService = Depends(PaymentService)
) -> Payment:
    with tracer.start_as_current_span("Create payment") as span:
        try:
            payment = payment_service.create_payment(payment_info.receiver, payment_info.sum,
                                                     PaymentType(payment_info.type))
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
