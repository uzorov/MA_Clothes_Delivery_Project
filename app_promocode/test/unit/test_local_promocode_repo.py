import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.promocode import Promocode
from app.repo.local_promocode_repo import PromocodeRepo

@pytest.fixture(scope='session')
def promo_repo() -> PromocodeRepo:
    return PromocodeRepo(clear=True)

@pytest.fixture(scope='session')
def first_promo() -> Promocode:
    code = 'test-code'
    discount = 0.2

    return Promocode(id=uuid4(), code=code, discount=discount)

@pytest.fixture(scope='session')
def second_promo() -> Promocode:
    code = 'test-code2'
    discount = 0.2

    return Promocode(id=uuid4(), code=code, discount=discount)



def test_empty_list(promo_repo: promo_repo) -> None:
    assert promo_repo.get_promocodes() == []

def test_create_new_promocode(promo_repo: promo_repo, first_promo: first_promo) -> None:
    created_promocode = promo_repo.create_promocode(first_promo.code, first_promo.discount)
    assert created_promocode.id is not None
    assert created_promocode.code == first_promo.code
    assert created_promocode.discount == first_promo.discount
    assert created_promocode in promo_repo.get_promocodes()

def test_get_existing_promocode(promo_repo: promo_repo, second_promo: second_promo) -> None:
    promo_repo.create_promocode(second_promo.code, second_promo.discount)
    discount = promo_repo.get_promocode(second_promo.code)
    assert discount == second_promo.discount

def test_create_duplicate_promocode(promo_repo: promo_repo, first_promo: first_promo) -> None:
    with pytest.raises(ValueError):
        promo_repo.create_promocode(first_promo.code, first_promo.discount)


