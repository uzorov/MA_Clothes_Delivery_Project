# /tests/unit/app_printing/services/test_printing_service.py

import pytest
from uuid import uuid4, UUID
from datetime import datetime
from app.services.printing_service import PrintingService
from app.models.printing import PrintingStatuses
from app.repositories.local_printing_repo import PrintingRepo


@pytest.fixture(scope='session')
def printing_service() -> PrintingService:
    return PrintingService(PrintingRepo(clear=True))


@pytest.fixture(scope='session')
def printing_id() -> UUID:
    return uuid4()


def test_create_first_printing(
    printing_id: UUID,
    printing_service: PrintingService
) -> None:
    date = datetime.now()
    printing = printing_service.create_printing(printing_id, date)
    assert printing.id == printing_id
    assert printing.date == date
    assert printing.status == PrintingStatuses.AWAITING


def test_create_first_printing_repeat(
    printing_id: UUID,
    printing_service: PrintingService
) -> None:
    date = datetime.now()
    with pytest.raises(KeyError):
        printing_service.create_printing(printing_id, date)


def test_get_printings_full(
    printing_id: UUID,
    printing_service: PrintingService
) -> None:
    printings = printing_service.get_printings()
    assert len(printings) == 1
    assert printings[0].id == printing_id


def test_begin_printing_not_found(
    printing_service: PrintingService
) -> None:
    with pytest.raises(KeyError):
        printing_service.begin_printing(uuid4())


def test_begin_printing(
    printing_id: UUID,
    printing_service: PrintingService
) -> None:
    printing = printing_service.begin_printing(printing_id)
    assert printing.status == PrintingStatuses.IN_PROCESS
    assert printing.id == printing_id

def test_finish_printing_not_found(
    printing_service: PrintingService
) -> None:
    with pytest.raises(KeyError):
        printing_service.finish_printing(uuid4())


def test_cancel_printing_not_found(
    printing_service: PrintingService
) -> None:
    with pytest.raises(KeyError):
        printing_service.cancel_printing(uuid4())


def test_cancel_printing(
    printing_id: UUID,
    printing_service: PrintingService
) -> None:
    printing = printing_service.cancel_printing(printing_id)
    assert printing.status == PrintingStatuses.CANCELED
    assert printing.id == printing_id
