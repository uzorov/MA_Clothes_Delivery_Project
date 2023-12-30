import pytest
from uuid import UUID, uuid4
from app.models.promocode import Promocode
from app.repo.db_promocode_repo import PromocodeRepo

@pytest.fixture()
def promocode_repo() -> PromocodeRepo:
    repo = PromocodeRepo()
    return repo


@pytest.fixture(scope='session')
def first_promocode() -> Promocode:
    return Promocode(id=uuid4(), code="TESTCODE1", discount=0.10)

@pytest.fixture(scope='session')
def second_promocode() -> Promocode:
    return Promocode(id=uuid4(), code="TESTCODE2", discount=0.20)


def test_add_first_promocode(first_promocode: Promocode, promocode_repo: PromocodeRepo) -> None:
    created_promocode=promocode_repo.create_promocode(first_promocode.code, first_promocode.discount)
    assert created_promocode.code == first_promocode.code


def test_add_second_promocode(first_promocode: Promocode, second_promocode: Promocode, promocode_repo: PromocodeRepo) -> None:
    created_promocode = promocode_repo.create_promocode(first_promocode.code, first_promocode.discount)
    assert created_promocode.code == first_promocode.code
    promocodes = promocode_repo.get_promocodes()
    assert len(promocodes) == 2
    assert promocodes[0] == first_promocode
    assert promocodes[1] == second_promocode
