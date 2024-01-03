import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.models.item import Item
from app.models.design import Design

def test_item_creation():
    name = "name"
    price = 5
    design = Design(id=uuid4(), image_url="")
    promocode = Item(id=uuid4(), name=name, price=price, design=design)
    assert isinstance(promocode.id, UUID)
    assert promocode.name == name
    assert promocode.price == price

def test_item_id_required():
    design = Design(id=uuid4(), image_url="")
    with pytest.raises(ValueError):
        Item(id=None, name="name", price=11, design=design)

def test_item_name_required():
    design = Design(id=uuid4(), image_url="")
    with pytest.raises(ValidationError):
        Item(id=uuid4(), name=None, price=0.1, design=design)

def test_item_price_type():
    design = Design(id=uuid4(), image_url="")
    with pytest.raises(ValidationError):
        Item(id=uuid4(), name="name", price="not_a_float", design=design)