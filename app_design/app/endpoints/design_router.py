from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.models.create_design_request import CreateDesignRequest
from app.services.design_service import DesignService
from app.models.design_model import Design



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
    resource=Resource.create({SERVICE_NAME: "design-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Design Service'
tracer = trace.get_tracer(name)


design_router = APIRouter(prefix='/designs', tags=['Designs'])


@design_router.get('/')
def get_designs(design_service: DesignService = Depends(DesignService)) -> list[Design]:
    with tracer.start_as_current_span("Get designs"):
        return design_service.get_designs()


@design_router.post('/')
def create_design(
        design_info: CreateDesignRequest,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    with tracer.start_as_current_span("Create design"):
        try:
            design = design_service.create_design(design_info.name, design_info.image_url)
            return design.dict()
        except KeyError:
            raise HTTPException(400, f'Design with name={design_info.name} already exists')


@design_router.put('/{id}/status')
def update_design_status(
        id: UUID, new_status: str,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    try:
        design = design_service.update_design_status(id, new_status)
        return design.dict()
    except KeyError:
        raise HTTPException(404, f'Design with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Invalid status: {new_status}')


@design_router.put('/{id}/image')
def update_design_image(
        id: UUID, new_image: str,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    try:
        design = design_service.update_design_image(id, new_image)
        return design.dict()
    except KeyError:
        raise HTTPException(404, f'Design with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Invalid image: {new_image}')


@design_router.delete('/{id}')
def delete_design(
        id: UUID,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    try:
        design = design_service.delete_design(id)
        return design.dict()
    except KeyError:
        raise HTTPException(404, f'Design with id={id} not found')
