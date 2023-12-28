import pytest
from uuid import UUID
from app.models.design_model import Design, DesignStatuses
from app.repositories.design_repo import DesignRepo

@pytest.fixture()
def design_repo() -> DesignRepo:
    repo = DesignRepo()
    return repo

@pytest.fixture(scope='session')
def sample_design() -> Design:
    return Design(
        id=UUID('00000000-0000-0000-0000-000000111111'),
        name='Sample Design',
        image_url='https://example.com/sample_design.jpg',
        status=DesignStatuses.AVAILABLE
    )

def test_create_design(design_repo: DesignRepo, sample_design: Design) -> None:
    created_design = design_repo.create_design(sample_design)
    assert created_design == sample_design

def test_get_design_by_id(design_repo: DesignRepo, sample_design: Design) -> None:
    retrieved_design = design_repo.get_design_by_id(sample_design.id)
    assert retrieved_design == sample_design

def test_set_status(design_repo: DesignRepo, sample_design: Design) -> None:
    new_status = DesignStatuses.UNAVAILABLE
    sample_design.status = new_status
    updated_design = design_repo.set_status(sample_design)
    assert updated_design.status == new_status

def test_delete_design(design_repo: DesignRepo, sample_design: Design) -> None:
    deleted_design = design_repo.delete_design(sample_design.id)
    assert deleted_design == sample_design
    assert sample_design not in design_repo.get_designs()