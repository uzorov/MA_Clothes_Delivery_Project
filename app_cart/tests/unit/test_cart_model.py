import pytest
from uuid import uuid4
from app.models.cart import Cart

@pytest.fixture()
def any_cart_uuid():
    return uuid4()

def test_cart_creation(any_cart_uuid):
    cart_data = {
        "id": str(any_cart_uuid),
        "items": [{"item_id": 1, "count": 2, "price": 10.0}],
        "total": 20.0,
        "user_id": str(any_cart_uuid),
        "status":"CREATED"
    }

    cart = Cart(**cart_data)

    assert cart.id == any_cart_uuid
    assert cart.items == [{"item_id": 1, "count": 2, "price": 10.0}]
    assert cart.total == 20.0

def test_cart_invalid_id(any_cart_uuid):
    cart_data = {
        "id": "1234",
        "items": [{"item_id": 1, "count": 2, "price": 10.0}],
        "total": 20.0,
        "user_id": str(any_cart_uuid)
    }

    with pytest.raises(ValueError):
        Cart(**cart_data)

def test_cart_invalid_items(any_cart_uuid):
    cart_data = {
        "id": str(any_cart_uuid),
        "items": "invalid items",
        "total": 20.0,
        "user_id": str(any_cart_uuid)
    }

    with pytest.raises(ValueError):
        Cart(**cart_data)

def test_cart_invalid_total(any_cart_uuid):
    cart_data = {
        "id": str(any_cart_uuid),
        "items": [{"item_id": 1, "count": 2, "price": 10.0}],
        "total": "invalid total",
        "user_id": str(any_cart_uuid)
    }

    with pytest.raises(ValueError):
        Cart(**cart_data)

