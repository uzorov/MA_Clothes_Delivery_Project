# tests/unit/test_design_service.py
import pytest
from uuid import uuid4, UUID
from app.services.design_service import DesignService
from app.models.design import Design
from app.repositories.design_repo import DesignRepo


@pytest.fixture(scope='session')
def design_service() -> DesignService:
    return DesignService(DesignRepo(clear=True))


@pytest.fixture()
def design_data() -> Design:
    return Design(
        id=uuid4(),
        image_url='sample_image.jpg',
    )



def test_create_design(
        design_data: Design,
        design_service: DesignService
) -> None:
    design = design_service.create_design(design_data.image_url)

    assert design.image_url == design_data.image_url


def test_delete_design(
        design_data: Design,
        design_service: DesignService
) -> None:
    design = design_service.create_design(design_data.image_url)
    deleted_design = design_service.delete_design(design.id)
    assert deleted_design == design
