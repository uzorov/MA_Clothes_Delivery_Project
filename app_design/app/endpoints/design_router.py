from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.models.create_design_request import CreateDesignRequest
from app.services.design_service import DesignService
from app.models.design_model import Design

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Команда запуска бобра
# docker run -d --name jaeger -e COLLECTOR_OTLP_ENABLED=true -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14250:14250 -p 14268:14268 -p 14269:14269 -p 4317:4317 -p 4318:4318 -p 9411:9411 jaegertracing/all-in-one:next-release
# opentelemetry-instrument --service_name design.api uvicorn app.main:app


provider = TracerProvider()

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

design_router = APIRouter(prefix='/designs', tags=['Designs'])


@design_router.get('/')
def get_designs(design_service: DesignService = Depends(DesignService)) -> list[Design]:
    with tracer.start_as_current_span("Get designs") as span:
        return design_service.get_designs()


@design_router.post('/')
def create_design(
        design_info: CreateDesignRequest,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    with tracer.start_as_current_span("Create design") as span:
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
