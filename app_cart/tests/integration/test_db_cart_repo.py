import pytest
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from app.models.cart import Cart, Item,CartStatuses
from app.schemas.cart import Cart as DBCart
from app.repo.db_cart_repo import CartRepo


@pytest.fixture(scope='session')
def cart_repo() -> CartRepo:
    return CartRepo()


@pytest.fixture(scope='session')
def sample_item() -> Item:
    return {"id":'f9a88108-699d-49c3-bcc4-795409506e37', "name":"Sample Item", "price":10.0, "count":2, "size":'s',}


def test_empty_carts(cart_repo: CartRepo) -> None:
    assert len(cart_repo.get_carts()) == 0


def test_create_cart(cart_repo: CartRepo, sample_item: dict) -> None:
    cart = Cart(id=uuid4(), items=[sample_item], total=sample_item['price'] * sample_item['count'],user_id=uuid4(),status=CartStatuses.CREATED)
    created_cart = cart_repo.create_cart(cart)
    assert created_cart.id is not None
    assert created_cart.total == cart.total


def test_update_cart(cart_repo: CartRepo, sample_item: dict) -> None:
    # Create a cart with a sample item
    initial_cart = Cart(id=uuid4(), items=[sample_item], total=sample_item['price'] * sample_item['count'],user_id=uuid4(),status=CartStatuses.CREATED)
    created_cart = cart_repo.create_cart(initial_cart)

    # Update the cart with another item
    updated_item = {"id":'f9a88108-699d-49c3-bcc4-795409506e37', "name":"new Item", "price":101.0, "count":2, "size":'m'}
    updated_cart = Cart(id=created_cart.id, items=[updated_item], total=updated_item['price'] * updated_item['count'] + initial_cart.total,user_id=created_cart.user_id,status=CartStatuses.CREATED)

    updated_cart = cart_repo.update_cart(updated_cart)

    assert updated_cart.id == created_cart.id
    assert len(updated_cart.items) == 1
    assert updated_cart.total == (sample_item['price'] * sample_item['count']) + (updated_item['price'] * updated_item['count'])


def test_get_carts(cart_repo: CartRepo, sample_item: dict) -> None:
    cart_repo.db.query(DBCart).delete()  # Clear the database before the test

    # Create two carts with sample items
    first_cart = Cart(id=uuid4(), items=[sample_item], total=sample_item['price'] * sample_item['count'],user_id=uuid4(),status=CartStatuses.CREATED)
    second_cart = Cart(id=uuid4(), items=[sample_item], total=sample_item['price'] * sample_item['count'],user_id=uuid4(),status=CartStatuses.CREATED)

    cart_repo.create_cart(first_cart)
    cart_repo.create_cart(second_cart)

    carts = cart_repo.get_carts()
    assert len(carts) == 2

    # Check the properties of the first cart
    first_cart = carts[0]
    assert first_cart.id is not None
    assert len(first_cart.items) == 1
    assert first_cart.total == sample_item['price'] * sample_item['count']


def test_get_cart_by_id(cart_repo: CartRepo, sample_item: dict) -> None:
    # Create a cart with a sample item
    initial_cart = Cart(id=uuid4(), items=[sample_item], total=sample_item['price'] * sample_item['count'],user_id=uuid4(),status=CartStatuses.CREATED)
    created_cart = cart_repo.create_cart(initial_cart)

    retrieved_cart = cart_repo.get_cart(created_cart.id)

    assert retrieved_cart is not None
    assert retrieved_cart.id == created_cart.id
    assert len(retrieved_cart.items) == 1
    assert retrieved_cart.total == sample_item['price'] * sample_item['count']
