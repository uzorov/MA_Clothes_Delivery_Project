import pytest
from uuid import uuid4, UUID
from app.models.cart import Cart, Item
from app.repo.db_cart_repo import CartRepo
from app.services.cart_service import CartService


@pytest.fixture(scope='session')
def cart_service() -> CartService:
    return CartService(CartRepo())


@pytest.fixture()
def cart_repo() -> CartRepo:
    return CartRepo()


@pytest.fixture(scope='session')
def sample_item() -> Item:
    return Item(id=uuid4(), name="Sample Item", price=10.0, count=2, size='s')


def test_create_cart(cart_service: CartService, sample_item: Item) -> None:
    cart = cart_service.create_cart(sample_item)
    assert cart.id is not None
    assert len(cart.items) == 1
    assert cart.total == sample_item.price * sample_item.count


def test_update_cart(cart_service: CartService, sample_item: Item) -> None:
    # Create a cart with a sample item
    cart = cart_service.create_cart(sample_item)

    # Update the cart with another item
    updated_item = Item(id=uuid4(), name="Updated Item", price=5.0, count=3, size='m')
    updated_cart = cart_service.update_cart(cart.id, updated_item)

    assert len(updated_cart.items) == 2
    assert updated_cart.total == (sample_item.price * sample_item.count) + (updated_item.price * updated_item.count)


def test_get_carts(cart_service: CartService, cart_repo: CartRepo, sample_item: Item) -> None:
    cart_service.create_cart(sample_item)
    cart_service.create_cart(sample_item)

    carts = cart_service.get_carts()

    first_cart = carts[0]
    assert first_cart.id is not None
    assert len(first_cart.items) == 1
    assert first_cart.total == sample_item.price * sample_item.count


def test_get_cart_by_id(cart_service: CartService, sample_item: Item) -> None:
    cart = cart_service.create_cart(sample_item)
    retrieved_cart = cart_service.get_cart_by_id(cart.id)

    assert retrieved_cart is not None
    assert retrieved_cart.id == cart.id
    assert len(retrieved_cart.items) == 1
    assert retrieved_cart.total == sample_item.price * sample_item.count
