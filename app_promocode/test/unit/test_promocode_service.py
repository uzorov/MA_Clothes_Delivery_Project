import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.promocode_service import PromocodeService
from app.repo.local_promocode_repo import PromocodeRepo


@pytest.fixture(scope='session')
def promo_service() -> PromocodeService:
    return PromocodeService(PromocodeRepo(clear=True))


@pytest.fixture(scope='session')
def first_promo_data() -> tuple[str, float]:
    return 'test-code1', 0.3


@pytest.fixture(scope='session')
def second_promo_data() -> tuple[str, float]:
    return 'test-code2', 0.2

def test_empty_books(promo_service: promo_service) -> None:
    assert promo_service.get_promocodes() == []

def test_add_first_promo(
    first_promo_data,
    promo_service: promo_service
    ) -> None:
    code, discount = first_promo_data
    promo_service.create_promocode(code, discount)
    promo = promo_service.get_promocodes()[0]
    assert promo.code == code
    assert promo.discount == discount

def test_add_second_promo(
    second_promo_data,
    promo_service: promo_service
    ) -> None:
    code, discount = second_promo_data
    promo_service.create_promocode(code, discount)
    promo = promo_service.get_promocodes()[1]
    assert promo.code == code
    assert promo.discount == discount

def test_get_nonexistent_promocode(promo_service: promo_service):
    with pytest.raises(ValueError):
        promo_service.get_promocode("invalid-code")

def test_create_duplicate_promocode(promo_service: promo_service, first_promo_data):
    with pytest.raises(ValueError):
        promo_service.create_promocode(*first_promo_data)


