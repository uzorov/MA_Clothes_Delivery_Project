import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.item import Item
from app.repositories.local_item_repo import ItemRepo

@pytest.fixture(scope='session')
def item_repo() -> ItemRepo:
    return ItemRepo(clear=True)

@pytest.fixture(scope='session')
def first_item() -> Item:
    name = 'футболка'
    price = 100
    design = "https://example.com/design"
    return Item(id=uuid4(), name=name, price=price, design=design)

@pytest.fixture(scope='session')
def second_item() -> Item:
    name = 'футболка2'
    price = 200
    design = "https://example.com/design"

    return Item(id=uuid4(), name=name, price=price, design=design)


def test_empty_list(item_repo: ItemRepo) -> None:
    assert item_repo.get_items() == []

def test_create_new_item(item_repo: ItemRepo, first_item) -> None:
    created_promocode = item_repo.create_item(first_item.name, first_item.price, first_item.design)
    assert created_promocode.id is not None
    assert created_promocode.name == first_item.name
    assert created_promocode.price == first_item.price
    assert created_promocode in item_repo.get_items()

def test_get_existing_item(item_repo: ItemRepo, second_item) -> None:
    item_repo.create_item(second_item.name, second_item.price,second_item.design)
    price = item_repo.get_item(second_item.name)
    assert price.name == second_item.name

def test_create_duplicate_item(item_repo: ItemRepo, first_item) -> None:
    with pytest.raises(ValueError):
        item_repo.create_item(first_item.name, first_item.price,first_item.design)


