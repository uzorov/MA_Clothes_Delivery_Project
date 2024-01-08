from uuid import UUID

import httpx
import prometheus_client
from app.models.printing import Printing, CreatePrintingRequest
from app.services.printing_service import PrintingService
from fastapi import APIRouter, Depends, HTTPException, Response, Header
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

delivery_service_url = "https://bbapu2gipilstlsge2kn.containers.yandexcloud.net"

def user_staff_admin(role):
    if role == "client" or role == "staff" or role == "admin":
        return True
    return False

def staff_admin(role):
    if role == "staff" or role == "admin":
        return True
    return False

def make_request_to_delivery_service(id):
    url = f"{delivery_service_url}/api/delivery/"
    print(str(id))
    data = {'id': str(id)}
    print(str(data))
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request to delivery: {response.status_code}, {response.text}")

@printing_router.get('/all')
def get_printings(printing_service: PrintingService = Depends(PrintingService), user: str = Header(...)) -> list[Printing]:
    user = eval(user)
    with tracer.start_as_current_span("Get printings"):
        if user['id'] is not None:
            if staff_admin(user['role']):
                get_printings_count.inc(1)
                return printing_service.get_printings()
            raise HTTPException(403)

@printing_router.get('/{id}')
def get_printing_by_id(id: UUID, printing_service: PrintingService = Depends(PrintingService), user: str = Header(...)) -> Printing:
    user = eval(user)
    with tracer.start_as_current_span("Get users printings"):
        if user['id'] is not None:
            if user_staff_admin(user['role']):
                get_printings_count.inc(1)
                return printing_service.get_printing_by_id(id)
            raise HTTPException(403)


@printing_router.post('/')
def add_printing(
        printing_info: CreatePrintingRequest,
        printing_service: PrintingService = Depends(PrintingService)
) -> Printing:
    with tracer.start_as_current_span("Add printing"):
        try:
            print(str(printing_info))
            printing = printing_service.create_printing(printing_info.id)
            #make_request_to_delivery_service(printing_info.id)
            created_printing_count.inc(1)
            return printing.dict()
        except KeyError:
            raise HTTPException(400, f'Printing with id={printing_info.id} already exists')


@printing_router.post('/{id}/begin')
def begin_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService), user: str = Header(...)) -> Printing:
    user = eval(user)
    try:
        if user['id'] is not None:
            if staff_admin(user['role']):
                printing = printing_service.begin_printing(id)
                started_printing_count.inc(1)
                return printing.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t begin')


@printing_router.post('/{id}/finish')
def finish_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService), user: str = Header(...)) -> Printing:
    user = eval(user)
    try:
        if user['id'] is not None:
            if staff_admin(user['role']):
                printing = printing_service.finish_printing(id)
                completed_printing_count.inc(1)
                return printing.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t be finished')



@printing_router.post('/{id}/cancel')
def cancel_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService), user: str = Header(...)) -> Printing:
    user = eval(user)
    try:
        if user['id'] is not None:
            if staff_admin(user['role']):
                printing = printing_service.cancel_printing(id)
                cancelled_printing_count.inc(1)
                return printing.dict()
            raise HTTPException(403)
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
