import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.models.promocode import Promocode

def test_promocode_creation():
    code = "TEST_CODE"
    discount = 0.1
    promocode = Promocode(id=uuid4(), code=code, discount=discount)
    assert isinstance(promocode.id, UUID)
    assert promocode.code == code
    assert promocode.discount == discount

def test_promocode_id_required():
    with pytest.raises(ValueError):
        Promocode(id=None, code="TEST_CODE", discount=0.1)

def test_promocode_code_required():
   
    with pytest.raises(ValidationError):
        Promocode(id=uuid4(), code=None, discount=0.1)

def test_promocode_discount_type():    
    with pytest.raises(ValidationError):
        Promocode(id=uuid4(), code="TEST_CODE", discount="not_a_float")
