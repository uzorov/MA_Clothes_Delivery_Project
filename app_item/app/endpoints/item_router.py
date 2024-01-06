from uuid import UUID
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Body, Query, Form
from typing import Optional, List
from app.services.item_service import ItemService
from app.models.item import Item
from app.services.design_service import DesignService
from app.models.item import Design
from enum import Enum
import httpx

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
        resource=Resource.create({SERVICE_NAME: "item-service"})
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

name = 'Item Service'
tracer = trace.get_tracer(name)


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


item_router = APIRouter(prefix='/item', tags=['Item'])
target_service_url = "http://app_cart:86"


def make_request_to_target_service(item_id, size, count, price, name):
    url = f"{target_service_url}/api/cart/"
    data = {"id": item_id, "size": size, "count": count, "price": price, "name": name}
    print(str(data))
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=data)
    if response.status_code == 200:
        return response.status_code
    else:
        raise Exception(f"Error making request:{response.status_code}, {response.text}")


class dropdownChoices(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"


@item_router.get('/')
def get_items(item_service: ItemService = Depends(ItemService)) -> list[Item]:
    with tracer.start_as_current_span("Get items") as span:
        add_endpoint_info(span, "/")
        try:
            add_operation_result(span, "success")
            return item_service.get_items()
        except Exception as e:
            add_operation_result(span, "failure")


@item_router.get('/{id}')
def get_items_by_id(id: str, item_service: ItemService = Depends(ItemService)) -> Item:
    with tracer.start_as_current_span("Get items by id") as span:
        add_endpoint_info(span, "/{id}")
        try:
            add_operation_result(span, "success")
            return item_service.get_items_by_id(id)
        except Exception as e:
            add_operation_result(span, f"failure: {str(e)}")


@item_router.post('/')
def create_item(
        name: str,
        price: float,
        design: str,
        item_service: ItemService = Depends(ItemService)) -> Item:
    with tracer.start_as_current_span("Create item") as span:
        add_endpoint_info(span, "/ [POST]")
        try:
            item = item_service.create_item(name, price, design)
            add_operation_result(span, "success")
            return item.dict()
        except KeyError:
            add_operation_result(span, "failure: Cant create item")
            raise HTTPException(404, f'Cant create item')


@item_router.post('/add_to_cart')
def add_to_cart(
        item_id: str,
        count: int,
        size: dropdownChoices = Form(dropdownChoices),
        item_service: ItemService = Depends(ItemService),
) -> Item:
    with tracer.start_as_current_span("Add to cart") as span:
        add_endpoint_info(span, "/add_to_cart")
        try:
            item = item_service.get_items_by_id(item_id)
            make_request_to_target_service(item_id, size, count, item.price, item.name)
            add_operation_result(span, "success")
            return item
        except KeyError:
            add_operation_result(span, "failure: Cant add to cart item")
            raise HTTPException(404, f'Cant add to cart item')


# ------------------ DESIGN ------------------

@item_router.put('/set-design/{id}')
def update_design_image(
        id: UUID, new_image: str,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    with tracer.start_as_current_span("Update design image") as span:
        add_endpoint_info(span, "/set-design/{id}")
        try:
            design = design_service.update_design_image(id, new_image)
            add_operation_result(span, "success")
            return design.dict()
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'Design with id={id} not found')
        except ValueError:
            add_operation_result(span, "failure")
            raise HTTPException(400, f'Invalid image: {new_image}')


@item_router.delete('/delete-design/{id}')
def delete_design(
        id: UUID,
        design_service: DesignService = Depends(DesignService)
) -> Design:
    with tracer.start_as_current_span("Delete design") as span:
        add_endpoint_info(span, "/delete-design/{id}")
        try:
            design = design_service.delete_design(id)
            add_operation_result(span, "success")
            return design.dict()
        except KeyError:
            add_operation_result(span, "failure")
            raise HTTPException(404, f'Design with id={id} not found')
