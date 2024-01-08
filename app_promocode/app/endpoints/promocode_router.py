from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
import asyncio

from app.services.promocode_service import PromocodeService
from app.models.promocode import Promocode
from app.rabbitmq import send_discount

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from app.settings import settings

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "promocode-Service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name=settings.host_ip,
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Promocode Service'
tracer = trace.get_tracer(name)

promocode_router = APIRouter(prefix='/promocode', tags=['Promocode'])

@promocode_router.get('/{code}')
def get_promocode(code: str, promocode_service: PromocodeService = Depends(PromocodeService)) -> Promocode:
    with tracer.start_as_current_span("Get promocode"):
        return promocode_service.get_promocode(code)

@promocode_router.get('/')
def get_promocodes(promocode_service: PromocodeService = Depends(PromocodeService)) -> list[Promocode]:
    with tracer.start_as_current_span("Get promocodes"):
        return promocode_service.get_promocodes()

@promocode_router.post('/')
def create_promocode(code: str, discount: float, promocode_service: PromocodeService = Depends(PromocodeService)) -> Promocode:
    try:
        order = promocode_service.create_promocode(code, discount)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Cant create promocode')
    
@promocode_router.post('/discount')
def set_discount(code: str, id: UUID, promocode_service: PromocodeService = Depends(PromocodeService)):
    try:
        discount = promocode_service.get_promocode(code)
        asyncio.run(send_discount(discount, id))
        return discount
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Да пошел ты нахуй')