import pytest
from uuid import UUID, uuid4
from app.models.design_model import Design, DesignStatuses
from app.repositories.design_repo import DesignRepo

@pytest.fixture(scope='session')
def design_repo() -> DesignRepo:
    return DesignRepo(clear=True)

@pytest.fixture(scope='session')
def sample_design() -> Design:
    return Design(
        id=uuid4(),
        name='Sample Design',
        image_url='https://example.com/sample_design.jpg',
        status=DesignStatuses.AVAILABLE
    )


def test_create_design(design_repo: DesignRepo, sample_design: Design) -> None:
    created_design = design_repo.create_design(sample_design)
    assert created_design == sample_design

def test_create_design_duplicate(design_repo: DesignRepo, sample_design: Design) -> None:
    with pytest.raises(KeyError):
        design_repo.create_design(sample_design)

def test_get_design_by_id(design_repo: DesignRepo, sample_design: Design) -> None:
    retrieved_design = design_repo.get_design_by_id(sample_design.id)
    assert retrieved_design == sample_design

def test_get_design_by_id_error(design_repo: DesignRepo) -> None:
    with pytest.raises(KeyError):
        design_repo.get_design_by_id(uuid4())

def test_set_status(design_repo: DesignRepo, sample_design: Design) -> None:
    sample_design.status = DesignStatuses.UNAVAILABLE
    updated_design = design_repo.set_status(sample_design)
    assert updated_design.status == DesignStatuses.UNAVAILABLE

    sample_design.status = DesignStatuses.AVAILABLE
    updated_design = design_repo.set_status(sample_design)
    assert updated_design.status == DesignStatuses.AVAILABLE
