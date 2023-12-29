from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.services.delivery_service import DeliveryService
from app.models.delivery import Delivery, CreateDeliveryRequest
import prometheus_client
from fastapi import Response

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
    resource=Resource.create({SERVICE_NAME: "delivery-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Delivery Service'
tracer = trace.get_tracer(name)


delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_deliveries_count = prometheus_client.Counter(
    "get_deliveries_count",
    "Total got all deliveries"
)

created_delivery_count = prometheus_client.Counter(
    "created_delivery_count",
    "Total created deliveries"
)

started_delivery_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started deliveries"
)

completed_delivery_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed deliveries"
)

cancelled_delivery_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled deliveries"
)


@delivery_router.get('/')
def get_deliveries(delivery_service: DeliveryService = Depends(DeliveryService)) -> list[Delivery]:
    with tracer.start_as_current_span("Get deliveries"):
        get_deliveries_count.inc(1)
        return delivery_service.get_deliveries()


@delivery_router.post('/')
def add_delivery(
        delivery_info: CreateDeliveryRequest,
        delivery_service: DeliveryService = Depends(DeliveryService)
) -> Delivery:
    with tracer.start_as_current_span("Add delivery"):
        try:
            delivery = delivery_service.create_delivery(delivery_info.id)
            created_delivery_count.inc(1)
            return delivery.dict()
        except KeyError:
            raise HTTPException(400, f'Delivery with id={delivery_info.id} already exists')


@delivery_router.post('/{id}/activate')
def activate_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.activate_delivery(id)
        started_delivery_count.inc(1)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be activated')


@delivery_router.post('/{id}/finish')
def finish_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.finish_delivery(id)
        completed_delivery_count.inc(1)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be finished')


@delivery_router.post('/{id}/cancel')
def cancel_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.cancel_delivery(id)
        cancelled_delivery_count.inc(1)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be canceled')


@delivery_router.post('/{id}/choose_pickup')
def choose_pickup(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.choose_pickup(id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} already has \'pickup\' type')


@delivery_router.post('/{id}/choose_delivery')
def choose_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.choose_delivery(id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} already has \'delivery\' type')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )