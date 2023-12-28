import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.payment_model import Payment, PaymentType


@pytest.fixture()
def any_payment_data() -> dict:
    return {
        'id': uuid4(),
        'receiver': 'John Doe',
        'sum': 100,
        'type': PaymentType.PC
    }


def test_payment_creation(any_payment_data: dict):
    payment = Payment(**any_payment_data)

    assert dict(payment) == any_payment_data


def test_payment_missing_receiver(any_payment_data: dict):
    any_payment_data.pop('receiver')

    with pytest.raises(ValidationError):
        Payment(**any_payment_data)


def test_payment_missing_sum(any_payment_data: dict):
    any_payment_data.pop('sum')

    with pytest.raises(ValidationError):
        Payment(**any_payment_data)


def test_payment_missing_type(any_payment_data: dict):
    any_payment_data.pop('type')

    with pytest.raises(ValidationError):
        Payment(**any_payment_data)


def test_payment_invalid_type(any_payment_data: dict):
    any_payment_data['type'] = 'invalid_type'

    with pytest.raises(ValidationError):
        Payment(**any_payment_data)
