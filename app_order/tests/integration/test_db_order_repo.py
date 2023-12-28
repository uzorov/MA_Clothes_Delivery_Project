import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.order import Order, OrderStatuses
from app.repositories.bd_order_repo import OrderRepo



@pytest.fixture()
def order_repo() -> OrderRepo:
    repo = OrderRepo()
    return repo

@pytest.fixture(scope='session')
def first_order() -> Order:
    id = uuid4()
    cart = uuid4()
    status = OrderStatuses.CREATED
    discount = 0.1
    price = 100.0

    return Order(id=id, cart=cart, status=status, discount=discount, price=price)

@pytest.fixture(scope='session')
def second_order() -> Order:
    id = uuid4()
    cart = uuid4()
    status = OrderStatuses.PAID
    discount = None
    price = 102.0

    return Order(id=id, cart=cart, status=status, discount=discount, price=price)


def test_empty_list(order_repo: order_repo) -> None:
    assert order_repo.get_orders() != []

def test_create_first_order(first_order: Order, order_repo: order_repo) -> None:
    assert order_repo.create_order(first_order) == first_order
    order = order_repo.get_orders()[-1]
    assert order == first_order

def test_get_book_by_id(order_repo: order_repo) -> None:
    order = order_repo.get_orders()[0]
    book_by_id = order_repo.get_order_by_id(order.id)
    assert order.id == book_by_id.id

def test_add_second_book(second_order: Order, order_repo: order_repo) -> None:
    assert order_repo.create_order(second_order) == second_order
    order = order_repo.get_orders()[-1]
    assert order == second_order

def test_set_status_valid(order_repo: order_repo, first_order: first_order) -> None:
    new_status = OrderStatuses.PAID
    order = first_order
    order.status = new_status
    order_repo.set_status(order)
    updated_order = order_repo.get_order_by_id(order.id)
    assert updated_order.status == new_status

def test_set_discount_valid(order_repo: order_repo, first_order: first_order) -> None:
    discount = 0.2
    order = first_order
    order.discount = discount
    order_repo.set_discount(order)
    updated_order = order_repo.get_order_by_id(order.id)
    assert updated_order.discount == discount

def test_delete_all_orders(order_repo: OrderRepo) -> None:
    assert len(order_repo.get_orders()) > 0
    order_repo.delete_all_orders()
    assert order_repo.get_orders() == []