import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.item import Item
from app.repositories.db_item_repo import ItemRepo

from app.models.design import Design
from app.repositories.design_repo import DesignRepo

sleep(5)


@pytest.fixture()
def item_repo() -> ItemRepo:
    item_repo = ItemRepo()
    return item_repo


@pytest.fixture()
def design_repo() -> DesignRepo:
    design_repo = DesignRepo()
    return design_repo


@pytest.fixture(scope='session')
def first_design() -> Design:
    id = uuid4()
    image_url = "https://test/design/1"

    return Design(id=id, image_url=image_url)


@pytest.fixture(scope='session')
def second_design() -> Design:
    id = uuid4()
    image_url = "https://test/design/2"

    return Design(id=id, image_url=image_url)


@pytest.fixture(scope='session')
def first_item() -> Item:
    id = uuid4()
    name = "Футболка 1"
    price = 399
    design = first_design()

    return Item(id=id, name=name, price=price, design=design)


@pytest.fixture(scope='session')
def second_item() -> Item:
    id = uuid4()
    name = "Футболка 2"
    price = 584
    design = second_design()

    return Item(id=id, name=name, price=price, design=design)


def test_empty_list(item_repo: ItemRepo) -> None:
    assert item_repo.get_items() != []


def test_add_first_item(first_item: Item, item_repo: ItemRepo) -> None:
    assert item_repo.create_item(first_item) == first_item


def test_get_item_by_id(first_item: Item, item_repo: ItemRepo) -> None:
    item = item_repo.get_books()[0]
    item_by_id = item_repo.get_item_by_id(item.id)
    assert item.id == item_by_id.id


def test_get_item_by_id_error(item_repo: ItemRepo) -> None:
    with pytest.raises(KeyError):
        item_repo.get_item_by_id(uuid4())


def test_add_second_item(first_item: Item, second_item: Item, item_repo: ItemRepo) -> None:
    assert item_repo.add_item(second_item) == second_item
    items = item_repo.get_items()
    assert items[len(items) - 1] == second_item

#test
