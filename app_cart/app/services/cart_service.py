from uuid import UUID
from datetime import datetime
from fastapi import Depends
from uuid import uuid4
from app.models.cart import Cart, Item
from app.repo.db_cart_repo import CartRepo


class CartService():
    cart_repo: CartRepo

    def __init__(self, cart_repo: CartRepo = Depends(CartRepo)) -> None:
        self.cart_repo = cart_repo

    def get_carts(self) -> list[Cart]:
        return self.cart_repo.get_carts()

    def get_cart_by_id(self, id: UUID):
        return self.cart_repo.get_cart(id)
    
    def create_cart(self, obj:Item) -> Cart:
        item = []
        di = obj.__dict__
        di['id'] = str(di['id'])
        total = di['price'] * di['count']
        item.append(obj.__dict__)
        cart = Cart(id=uuid4(), items=item, total=total)
        return self.cart_repo.create_cart(cart)
    
    def update_cart(self, id:UUID, obj:Item):
        cart = self.get_cart_by_id(id)
        di = obj.__dict__
        di['id'] = str(di['id'])
        cart.total = di['price'] * di['count'] + cart.total
        cart.items.append(obj.__dict__)
        return self.cart_repo.update_cart(cart)
