

import pytest
from uuid import UUID, uuid4
from time import sleep
from datetime import datetime
from app.models.printing import Printing, PrintingStatuses
from app.repositories.db_printing_repo import PrintingRepo

sleep(5)


@pytest.fixture()
def printing_repo() -> PrintingRepo:
    repo = PrintingRepo()
    return repo


@pytest.fixture(scope='session')
def printing_id() -> UUID:
    return uuid4()


@pytest.fixture(scope='session')
def first_printing() -> Printing:
    return Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)


@pytest.fixture(scope='session')
def second_printing() -> Printing:
    return Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)


def test_empty_list(printing_repo: PrintingRepo) -> None:
    printing_repo.delete_all_printings()
    assert printing_repo.get_printings() == []


def test_add_first_printing(first_printing: Printing, printing_repo: PrintingRepo) -> None:
    assert printing_repo.create_printing(first_printing) == first_printing


def test_add_first_printing_repeat(first_printing: Printing, printing_repo: PrintingRepo) -> None:
    with pytest.raises(KeyError):
        printing_repo.create_printing(first_printing)


def test_get_printing_by_id(first_printing: Printing, printing_repo: PrintingRepo) -> None:
    assert printing_repo.get_printing_by_id(
        first_printing.id) == first_printing


def test_get_printing_by_id_error(printing_repo: PrintingRepo) -> None:
    with pytest.raises(KeyError):
        printing_repo.get_printing_by_id(uuid4())


def test_add_second_printing(first_printing: Printing, second_printing: Printing, printing_repo: PrintingRepo) -> None:
    assert printing_repo.create_printing(second_printing) == second_printing
    printings = printing_repo.get_printings()
    assert len(printings) == 2
    assert printings[0] == first_printing
    assert printings[1] == second_printing


def test_set_status(first_printing: Printing, printing_repo: PrintingRepo) -> None:
    first_printing.status = PrintingStatuses.IN_PROCESS
    assert printing_repo.set_status(
        first_printing).status == first_printing.status

    first_printing.status = PrintingStatuses.DONE
    assert printing_repo.set_status(
        first_printing).status == first_printing.status

    first_printing.status = PrintingStatuses.AWAITING
    assert printing_repo.set_status(
        first_printing).status == first_printing.status
