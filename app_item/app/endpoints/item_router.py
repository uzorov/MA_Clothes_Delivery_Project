from uuid import UUID
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Body, Query, Form
from typing import Optional, List
from app.services.item_service import ItemService
from app.models.item import Item
from app.services.design_service import DesignService
from app.models.item  import Design
from enum import Enum
import httpx

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
        resource=Resource.create({SERVICE_NAME: "item-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

name = 'Item Service'
tracer = trace.get_tracer(name)

item_router = APIRouter(prefix='/item', tags=['Item'])
target_service_url = "http://app_cart:86"


def make_request_to_target_service(item_id,size,count,price,name):
    url = f"{target_service_url}/api/cart/"
    data = {"id": item_id, "size": size, "count": count, "price": price, "name": name}
    print(str(data))
    with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request: {response.status_code}, {response.text}")


class dropdownChoices(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"


@item_router.get('/')
def get_items(item_service: ItemService = Depends(ItemService)) -> list[Item]:
    return item_service.get_items()


@item_router.get('/{id}')
def get_items_by_id(id: str, item_service: ItemService = Depends(ItemService)) -> Item:
    return item_service.get_items_by_id(id)


@item_router.post('/')
def create_item(
        name: str,
        price: float,
        design: str,
        item_service: ItemService = Depends(ItemService)) -> Item:
    with tracer.start_as_current_span("Create item"):
        try:
            item = item_service.create_item(name, price, design)
            return item.dict()
        except KeyError:
            raise HTTPException(404, f'Cant create item')


@item_router.post('/add_to_cart')
async def add_to_cart(
        item_id: str,
        count: int,
        size: dropdownChoices = Form(dropdownChoices),
        item_service: ItemService = Depends(ItemService),
        ) -> Item:
    with tracer.start_as_current_span("Add to cart"):
        try:
            item = item_service.get_items_by_id(item_id)
            make_request_to_target_service(item_id,size,count,item.price,item.name)
            return item
        except KeyError:
            raise HTTPException(404, f'Cant add to cart item')


# ------------------ DESIGN ------------------

@item_router.put('/set-design/{id}')
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


@item_router.delete('/delete-design/{id}')
def delete_design(
        id: UUID,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    try:
        design = design_service.delete_design(id)
        return design.dict()
    except KeyError:
        raise HTTPException(404, f'Design with id={id} not found')
