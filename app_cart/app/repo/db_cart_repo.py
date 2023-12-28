import traceback
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException, Body
from app.database import get_db
from app.models.cart import Cart
from app.schemas.cart import Cart as DBCart
import logging

logging.basicConfig()

class CartRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())
    
    def _map_to_model(self, cart: DBCart) -> Cart:
        result = Cart.from_orm(cart)
        return result

    def _map_to_schema(self, cart: Cart) -> DBCart:
        data = dict(cart)
        result = DBCart(**data)
        return result

    def get_carts(self) -> list[Cart]:
        carts = []
        for c in self.db.query(DBCart).all():
            carts.append(self._map_to_model(c))
        return carts
    
    def get_cart(self, id:UUID) -> Cart:
        cart = self.db \
            .query(DBCart) \
            .filter(DBCart.id == id) \
            .first()
        if cart is None:
            raise KeyError
        return self._map_to_model(cart)

    def create_cart(self, cart: Cart) -> Cart:
        try:
            db_cart = self._map_to_schema(cart)
            self.db.add(db_cart)
            self.db.commit()
            return self._map_to_model(db_cart)
        except:
            traceback.print_exc()
            raise KeyError
    
    def update_cart(self, cart:Cart) -> Cart:
        try:
            db_cart = self.db.query(DBCart).filter(DBCart.id == cart.id).first()
            db_cart.total = cart.total
            db_cart.items = cart.items
            self.db.commit()
            return self.db.query(DBCart).filter(DBCart.id == cart.id).first()
        except:
            traceback.print_exc()
            raise KeyError

