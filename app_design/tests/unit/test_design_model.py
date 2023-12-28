import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.design_model import Design, DesignStatuses


@pytest.fixture()
def any_design_data() -> dict:
    return {
        'id': uuid4(),
        'name': 'Design Name',
        'image_url': 'https://example.com/image.jpg',
        'status': DesignStatuses.AVAILABLE
    }


def test_design_creation(any_design_data: dict):
    design = Design(**any_design_data)

    assert dict(design) == any_design_data


def test_design_missing_name(any_design_data: dict):
    any_design_data.pop('name')

    with pytest.raises(ValidationError):
        Design(**any_design_data)


def test_design_missing_image_url(any_design_data: dict):
    any_design_data.pop('image_url')

    with pytest.raises(ValidationError):
        Design(**any_design_data)


def test_design_invalid_status(any_design_data: dict):
    any_design_data['status'] = 'invalid_status'

    with pytest.raises(ValidationError):
        Design(**any_design_data)
