# /tests/unit/test_printing_repo.py

import pytest
from uuid import uuid4
from datetime import datetime

from app.models.printing import Printing, PrintingStatuses
from app.repositories.local_printing_repo import PrintingRepo


printing_test_repo = PrintingRepo()


def test_empty_list() -> None:
    assert printing_test_repo.get_printings() == []


def test_add_first_printing() -> None:
    printing = Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)
    assert printing_test_repo.create_printing(printing) == printing


def test_add_first_printing_repeat() -> None:
    printing = Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)
    printing_test_repo.create_printing(printing)
    with pytest.raises(KeyError):
        printing_test_repo.create_printing(printing)


def test_get_printing_by_id() -> None:
    printing = Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)
    printing_test_repo.create_printing(printing)
    assert printing_test_repo.get_printing_by_id(printing.id) == printing


def test_get_printing_by_id_error() -> None:
    with pytest.raises(KeyError):
        printing_test_repo.get_printing_by_id(uuid4())


def test_set_status() -> None:
    printing = Printing(id=uuid4(), date=datetime.now(), status=PrintingStatuses.AWAITING)
    printing_test_repo.create_printing(printing)

    printing.status = PrintingStatuses.IN_PROCESS
    assert printing_test_repo.set_status(printing).status == printing.status

    printing.status = PrintingStatuses.CANCELED
    assert printing_test_repo.set_status(printing).status == printing.status

    printing.status = PrintingStatuses.DONE
    assert printing_test_repo.set_status(printing).status == printing.status

    printing.status = PrintingStatuses.AWAITING
    assert printing_test_repo.set_status(printing).status == printing.status
