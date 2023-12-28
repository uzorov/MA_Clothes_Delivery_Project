# /tests/unit/test_printing_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.printing import Printing, PrintingStatuses


def test_printing_creation():
    id = uuid4()
    date = datetime.now()
    status = PrintingStatuses.DONE
    printing = Printing(id=id, date=date, status=status)

    assert dict(printing) == {'id': id, 'date': date, 'status': status}


def test_printing_date_required():
    with pytest.raises(ValidationError):
        Printing(id=uuid4(), status=PrintingStatuses.AWAITING)


def test_printing_status_required():
    with pytest.raises(ValidationError):
        Printing(id=uuid4(), date=datetime.now())
