import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.models.item import Item

def test_item_creation():
    name = "name"
    price = 5
    promocode = Item(id=uuid4(), name=name, price=price)
    assert isinstance(promocode.id, UUID)
    assert promocode.name == name
    assert promocode.price == price

def test_item_id_required():
    with pytest.raises(ValueError):
        Item(id=None, name="name", price=11)

def test_item_name_required():
   
    with pytest.raises(ValidationError):
        Item(id=uuid4(), name=None, price=0.1)

def test_item_price_type():    
    with pytest.raises(ValidationError):
        Item(id=uuid4(), name="name", price="not_a_float")