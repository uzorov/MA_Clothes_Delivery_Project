# tests/unit/test_design_service.py
import pytest
from uuid import uuid4, UUID
from app.services.design_service import DesignService
from app.models.design_model import DesignStatuses, Design
from app.repositories.design_repo import DesignRepo


@pytest.fixture(scope='session')
def design_service() -> DesignService:
    return DesignService(DesignRepo(clear=True))


@pytest.fixture()
def design_data() -> Design:
    return Design(
        id=uuid4(),
        name='Design',
        image_url='sample_image.jpg',
        status=DesignStatuses.AVAILABLE
    )


def test_empty_designs(design_service: DesignService) -> None:
    assert design_service.get_designs() == []


def test_create_design(
        design_data: Design,
        design_service: DesignService
) -> None:
    design = design_service.create_design(design_data.name, design_data.image_url)

    assert design.name == design_data.name
    assert design.image_url == design_data.image_url
    assert design.status == DesignStatuses.AVAILABLE


def test_update_design_status(
        design_data: Design,
        design_service: DesignService
) -> None:
    designs = design_service.get_designs()
    design_data = designs[0]
    new_status = DesignStatuses.UNAVAILABLE
    design_service.update_design_status(design_data.id, new_status)
    design = design_service.get_design_by_id(design_data.id)
    assert design.status == new_status


def test_delete_design(
        design_data: Design,
        design_service: DesignService
) -> None:
    designs = design_service.get_designs()
    design_data = designs[0]
    design_service.delete_design(design_data.id)
    designs = design_service.get_designs()
    assert len(designs) == 0


def test_get_design_by_id(
        design_data: Design,
        design_service: DesignService
) -> None:
    design = design_service.create_design(design_data.name, design_data.image_url)
    designs = design_service.get_designs()
    design_data = designs[0]
    design = design_service.get_design_by_id(design_data.id)
    assert design.id == design_data.id
    assert design.name == design_data.name
    assert design.image_url == design_data.image_url
    assert design.status == DesignStatuses.AVAILABLE