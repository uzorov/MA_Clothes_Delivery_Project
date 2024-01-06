# /tests/integration/app_repositories/test_db_delivery_repo.py

import pytest
from uuid import UUID, uuid4
from datetime import datetime
from app.models.delivery import Delivery, DeliveryStatuses, DeliveryTypes
from app.repositories.db_delivery_repo import DeliveryRepo


@pytest.fixture()
def delivery_repo() -> DeliveryRepo:
    repo = DeliveryRepo()
    return repo


@pytest.fixture(scope='session')
def delivery_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_delivery() -> Delivery:
    return Delivery(id=uuid4(), date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.STANDARD)


@pytest.fixture(scope='session')
def second_delivery() -> Delivery:
    return Delivery(id=uuid4(), date=datetime.now(), status=DeliveryStatuses.CREATED, type=DeliveryTypes.EXPRESS)


def test_empty_list(delivery_repo: DeliveryRepo) -> None:
    delivery_repo.delete_all_deliveries()
    assert delivery_repo.get_deliveries() == []


def test_add_first_delivery(first_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    assert delivery_repo.create_delivery(first_delivery) == first_delivery


def test_add_first_delivery_repeat(first_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    with pytest.raises(KeyError):
        delivery_repo.create_delivery(first_delivery)


def test_get_delivery_by_id(first_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    assert delivery_repo.get_delivery_by_id(first_delivery.id) == first_delivery


def test_get_delivery_by_id_error(delivery_repo: DeliveryRepo) -> None:
    with pytest.raises(KeyError):
        delivery_repo.get_delivery_by_id(uuid4())


def test_add_second_delivery(first_delivery: Delivery, second_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    assert delivery_repo.create_delivery(second_delivery) == second_delivery
    deliveries = delivery_repo.get_deliveries()
    assert len(deliveries) == 2
    assert deliveries[0] == first_delivery
    assert deliveries[1] == second_delivery


def test_set_status(first_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    first_delivery.status = DeliveryStatuses.IN_PROCESS
    assert delivery_repo.set_status(first_delivery).status == first_delivery.status



def test_set_type(first_delivery: Delivery, delivery_repo: DeliveryRepo) -> None:
    first_delivery.type = DeliveryTypes.DELIVERY
    assert delivery_repo.set_type(first_delivery).type == first_delivery.type
