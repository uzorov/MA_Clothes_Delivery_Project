# /tests/unit/test_delivery_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.delivery import Delivery, DeliveryStatuses, DeliveryTypes


def test_delivery_creation():
    id = uuid4()
    address = 'Test Address'
    date = datetime.now()
    status = DeliveryStatuses.DONE
    delivery_type = DeliveryTypes.DELIVERY

    delivery = Delivery(id=id, address=address, date=date, status=status, type=delivery_type)

    assert dict(delivery) == {'id': id, 'address': address, 'date': date, 'status': status, 'type': delivery_type}


def test_delivery_address_required():
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)


def test_delivery_date_required():
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), address='Test Address', status=DeliveryStatuses.CREATED, type=DeliveryTypes.DELIVERY)


def test_delivery_status_required():
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), address='Test Address', date=datetime.now(), type=DeliveryTypes.PICKUP)


def test_delivery_type_required():
    with pytest.raises(ValidationError):
        Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED)
