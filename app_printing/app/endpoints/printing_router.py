from uuid import UUID

import httpx
import prometheus_client
from app.models.printing import Printing, CreatePrintingRequest
from app.services.printing_service import PrintingService
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse

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
    resource=Resource.create({SERVICE_NAME: "printing-Service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Printing Service'
tracer = trace.get_tracer(name)

printing_router = APIRouter(prefix='/printing', tags=['Printing'])
metrics_router = APIRouter(tags=['Metrics'])


get_printings_count = prometheus_client.Counter(
    "get_printings_count",
    "Total got all printings"
)

created_printing_count = prometheus_client.Counter(
    "created_printing_count",
    "Total created printings"
)

started_printing_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started printings"
)

completed_printing_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed printings"
)

cancelled_printing_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled printings"
)


@printing_router.get('/')
def get_printings(printing_service: PrintingService = Depends(PrintingService)) -> list[Printing]:
    with tracer.start_as_current_span("Get printings"):
        get_printings_count.inc(1)
        return printing_service.get_printings()



@printing_router.post('/')
def add_printing(
        printing_info: CreatePrintingRequest,
        printing_service: PrintingService = Depends(PrintingService)
) -> Printing:
    with tracer.start_as_current_span("Add printing"):
        try:
            printing = printing_service.create_printing(printing_info.id, printing_info.date)
            created_printing_count.inc(1)
            return printing.dict()
        except KeyError:
            raise HTTPException(400, f'Printing with id={printing_info.id} already exists')


@printing_router.post('/{id}/begin')
def begin_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:
        printing = printing_service.begin_printing(id)
        started_printing_count.inc(1)
        return printing.dict()
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t begin')


@printing_router.post('/{id}/finish')
def finish_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:

        printing = printing_service.finish_printing(id)
        completed_printing_count.inc(1)
        return printing.dict()
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t be finished')



@printing_router.post('/{id}/cancel')
def cancel_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:
        printing = printing_service.cancel_printing(id)
        cancelled_printing_count.inc(1)
        return printing.dict()
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t be canceled')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
