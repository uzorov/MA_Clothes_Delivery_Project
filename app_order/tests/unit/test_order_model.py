import pytest
from uuid import uuid4
from app.models.order import Order, OrderStatuses


@pytest.fixture()
def any_cart_uuid():
    return uuid4()


def test_order_creation(any_cart_uuid):
    order_data = {
        "cart": str(any_cart_uuid),
        "status": OrderStatuses.DONE,
        "discount": 0.1,
        "price": 100.0,
    }

    order = Order(**order_data)

    assert order.cart == any_cart_uuid
    assert order.status == OrderStatuses.DONE
    assert order.discount == 0.1
    assert order.price == 100.0



def test_order_invalid_id_cart(any_cart_uuid):
    order_data = {
        "cart": "1234",
        "price": 100.0,
        "status": OrderStatuses.DONE,
        "discount": 0.1,
    }

    with pytest.raises(ValueError):
        Order(**order_data)


def test_order_invalid_price(any_cart_uuid):
    order_data = {
        "cart": str(any_cart_uuid),
        "price": 'invalid price',
        "status": OrderStatuses.DONE,
        "discount": 0.1,
    }

    with pytest.raises(ValueError):
        Order(**order_data)


def test_order_invalid_status(any_cart_uuid):
    order_data = {
        "cart": str(any_cart_uuid),
        "price": 100.0,
        "status": "invalid status",
        "discount": 0.1,
    }

    with pytest.raises(ValueError):
        Order(**order_data)


def test_order_invalid_discount(any_cart_uuid):
    order_data = {
        "cart": str(any_cart_uuid),
        "price": 100.0,
        "status": OrderStatuses.DONE,
        "discount": "invalid discount",
    }

    with pytest.raises(ValueError):
        Order(**order_data)


def test_order_with_no_cart_id():
    order_data = {
        "price": 100.0,
        "status": "invalid status",
        "discount": 0.1,
    }

    with pytest.raises(ValueError):
        Order(**order_data)

