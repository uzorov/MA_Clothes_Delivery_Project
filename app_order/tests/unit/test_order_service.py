import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.models.order import Order, OrderStatuses
from app.services.order_service import OrderService
from app.repositories.bd_order_repo import OrderRepo

@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService(OrderRepo())

@pytest.fixture()
def order_repo() -> OrderRepo:
    return OrderRepo()

@pytest.fixture(scope='session')
def first_order_data() -> tuple[UUID, float]:
    return uuid4(), 132

@pytest.fixture(scope='session')
def second_order_data() -> tuple[UUID, float]:
    return uuid4(), 122.12


def test_empty_orders(order_service: order_service, order_repo: order_repo) -> None:
    order_repo.delete_all_orders()
    assert order_service.get_orders() == []


def test_create_order(
        first_order_data,
        order_service: order_service
) -> None:
    cart, price = first_order_data
    order_service.create_order(cart, price)
    order = order_service.get_orders()[0]
    assert order.cart == cart
    assert order.price == price
    assert order.status == OrderStatuses.CREATED
    assert order.discount == None


def test_create_second_order(
        second_order_data,
        order_service: order_service
) -> None:
    cart, price = second_order_data
    order_service.create_order(cart, price)
    order = order_service.get_orders()[1]
    assert order.cart == cart
    assert order.price == price
    assert order.status == OrderStatuses.CREATED
    assert order.discount == None


def test_get_orders(
        first_order_data, second_order_data,
        order_service: order_service, order_repo: order_repo
    ) -> None:
    order_repo.delete_all_orders()
    
    cart_1, price_1 = first_order_data
    cart_2, price_2 = second_order_data
   
    order_service.create_order(cart_1, price_1)
    order_service.create_order(cart_2, price_2)
    orders = order_service.get_orders()
    assert len(orders) == 2

    order_1 = orders[0]
    assert order_1.cart == cart_1
    assert order_1.price == price_1
    assert order_1.status == OrderStatuses.CREATED
    assert order_1.discount == None

    order_2 = orders[1]
    assert order_2.cart == cart_2
    assert order_2.price == price_2
    assert order_2.status == OrderStatuses.CREATED
    assert order_2.discount == None


def test_get_order_by_id_existing_order(
    first_order_data, order_service: order_service
) -> None:
    cart_id, price = first_order_data
    order = order_service.get_orders()[0]
    order_by_id = order_service.get_order_by_id(str(order.id))
    assert order_by_id is not None
    assert order_by_id.cart == cart_id
    assert order_by_id.price == price
    assert order_by_id.status == OrderStatuses.CREATED
    assert order_by_id.discount is None

def test_get_order_by_id_nonexistent_order(order_service: order_service) -> None:
    with pytest.raises(KeyError):
        order_service.get_order_by_id(uuid4())


def test_paid_order_valid(order_service: order_service) -> None:
    order = order_service.get_orders()[0]
    order = order_service.paid_order(str(order.id))
    assert order.status == OrderStatuses.PAID


def test_set_discount_valid(order_service: order_service) -> None:
    discount = 0.1
    order = order_service.get_orders()[0]
    order = order_service.set_discount(str(order.id), discount)
    assert order.discount == discount


def test_finish_order_valid(order_service: order_service) -> None:
    order = order_service.get_orders()[0]
    order = order_service.finish_order(str(order.id))
    assert order.status == OrderStatuses.DONE