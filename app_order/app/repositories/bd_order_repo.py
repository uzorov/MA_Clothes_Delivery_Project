import traceback
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException, Body
from app.database import get_db
from app.models.order import Order, OrderStatuses
from app.schemas.order import Order as DBOrder


logging.basicConfig(level=logging.INFO)


class OrderRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)
        return result

    def _map_to_schema(self, order: Order) -> DBOrder:
        data = dict(order)
        result = DBOrder(**data)
        return result

    def get_user_orders(self, user_id: UUID) -> list[Order]:
        orders = []
        for d in self.db.query(DBOrder).filter(DBOrder.user_id == user_id):
            orders.append(self._map_to_model(d))
        return orders

    def get_user_order_by_id(self, id: UUID, user_id: UUID) -> Order:
        order = self.db \
            .query(DBOrder) \
            .filter(DBOrder.id == id and DBOrder.user_id == user_id) \
            .first()
        if order is None:
            raise KeyError
        return self._map_to_model(order)
    
    def get_order_by_id(self, id: UUID) -> Order:
        order = self.db \
            .query(DBOrder) \
            .filter(DBOrder.id == id) \
            .first()
        if order is None:
            raise KeyError
        return self._map_to_model(order)

    def create_order(self, order: Order) -> Order:
        try:
            db_order = self._map_to_schema(order)
            self.db.add(db_order)
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError
    
    def set_status(self, order: Order) -> Order:
        try:
            db_order = self.db.query(DBOrder).filter(DBOrder.id == order.id).first()
            db_order.status = order.status
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError

    def set_discount(self, order: Order) -> Order:
        try:
            db_order = self.db.query(DBOrder).filter(DBOrder.id == order.id).first()
            db_order.discount = order.discount
            self.db.commit()
            return self._map_to_model(db_order)
        except:
            traceback.print_exc()
            raise KeyError
    
    def delete_all_orders(self) -> None:
        self.db.query(DBOrder).delete()
        self.db.commit()