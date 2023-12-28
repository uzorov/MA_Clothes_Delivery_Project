# /tests/unit/test_delivery_repo.py

import pytest
from uuid import uuid4
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses, DeliveryTypes
from app.repositories.local_delivery_repo import DeliveryRepo


delivery_test_repo = DeliveryRepo()


def test_empty_list() -> None:
    assert delivery_test_repo.get_deliveries() == []


def test_add_first_delivery() -> None:
    delivery = Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)
    assert delivery_test_repo.create_delivery(delivery) == delivery


def test_add_first_delivery_repeat() -> None:
    delivery = Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)
    delivery_test_repo.create_delivery(delivery)
    with pytest.raises(KeyError):
        delivery_test_repo.create_delivery(delivery)


def test_get_delivery_by_id() -> None:
    delivery = Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)
    delivery_test_repo.create_delivery(delivery)
    assert delivery_test_repo.get_delivery_by_id(delivery.id) == delivery


def test_get_delivery_by_id_error() -> None:
    with pytest.raises(KeyError):
        delivery_test_repo.get_delivery_by_id(uuid4())


def test_set_status() -> None:
    delivery = Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)
    delivery_test_repo.create_delivery(delivery)

    delivery.status = DeliveryStatuses.IN_PROCESS
    assert delivery_test_repo.set_status(delivery).status == delivery.status

    delivery.status = DeliveryStatuses.CANCELED
    assert delivery_test_repo.set_status(delivery).status == delivery.status

    delivery.status = DeliveryStatuses.DONE
    assert delivery_test_repo.set_status(delivery).status == delivery.status

    delivery.status = DeliveryStatuses.CREATED
    assert delivery_test_repo.set_status(delivery).status == delivery.status


def test_set_type() -> None:
    delivery = Delivery(id=uuid4(), address='Test Address', date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.PICKUP)
    delivery_test_repo.create_delivery(delivery)

    delivery.type = DeliveryTypes.DELIVERY
    assert delivery_test_repo.set_type(delivery).type == delivery.type

    delivery.type = DeliveryTypes.PICKUP
    assert delivery_test_repo.set_type(delivery).type == delivery.type
