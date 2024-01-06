import pytest
from uuid import UUID, uuid4
from app.models.promocode import Promocode
from app.repo.db_promocode_repo import PromocodeRepo

@pytest.fixture()
def promocode_repo() -> PromocodeRepo:
    repo = PromocodeRepo()
    return repo


@pytest.fixture(scope='session')
def promocode() -> Promocode:
    return Promocode(id=uuid4(), code="TESTCODE", discount=0.10)

def test_empty_list(promocode_repo: PromocodeRepo) -> None:
    assert promocode_repo.get_promocodes() == []

def test_add_promocode(promocode: Promocode, promocode_repo: PromocodeRepo) -> None:
    created_promocode=promocode_repo.create_promocode(promocode.code, promocode.discount)
    assert created_promocode.code == promocode.code


