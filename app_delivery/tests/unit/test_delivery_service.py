# /tests/unit/app_delivery/services/test_delivery_service.py

import pytest
from uuid import uuid4, UUID
from datetime import datetime
from app.services.delivery_service import DeliveryService
from app.models.delivery import DeliveryStatuses, DeliveryTypes
from app.repositories.local_delivery_repo import DeliveryRepo


@pytest.fixture(scope='session')
def delivery_service() -> DeliveryService:
    return DeliveryService(DeliveryRepo(clear=True))


@pytest.fixture(scope='session')
def delivery_id() -> UUID:
    return uuid4()


def test_create_first_delivery(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.create_delivery(delivery_id)
    assert delivery.id == delivery_id
    assert delivery.address == "To Be Chosen"
    assert delivery.date == "2000-01-01 00:00:00.000"
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.type == DeliveryTypes.PICKUP


def test_create_first_delivery_repeat(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.create_delivery(delivery_id)


def test_get_deliveries_full(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    deliveries = delivery_service.get_deliveries()
    assert len(deliveries) == 1
    assert deliveries[0].id == delivery_id


def test_activate_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.activate_delivery(uuid4())


def test_activate_delivery(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.activate_delivery(delivery_id)
    assert delivery.status == DeliveryStatuses.IN_PROCESS
    assert delivery.id == delivery_id


def test_finish_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.finish_delivery(uuid4())


def test_cancel_delivery_not_found(
    delivery_service: DeliveryService
) -> None:
    with pytest.raises(KeyError):
        delivery_service.cancel_delivery(uuid4())


def test_cancel_delivery(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.cancel_delivery(delivery_id)
    assert delivery.status == DeliveryStatuses.CANCELED
    assert delivery.id == delivery_id


def test_choose_pickup(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.choose_pickup(delivery_id)
    assert delivery.type == DeliveryTypes.PICKUP
    assert delivery.id == delivery_id


def test_choose_delivery(
    delivery_id: UUID,
    delivery_service: DeliveryService
) -> None:
    delivery = delivery_service.choose_delivery(delivery_id)
    assert delivery.type == DeliveryTypes.DELIVERY
    assert delivery.id == delivery_id
