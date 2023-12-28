from uuid import UUID
from datetime import datetime
from fastapi import Depends
from uuid import uuid4
from app.models.order import Order, OrderStatuses
from app.repositories.bd_order_repo import OrderRepo


class OrderService():
    order_repo: OrderRepo

    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo)) -> None:
        self.order_repo = order_repo

    def get_user_orders(self, user_id: UUID) -> list[Order]:
        return self.order_repo.get_user_orders(user_id)
    
    def get_order_by_id(self, order_id: UUID):
        return self.order_repo.get_order_by_id(order_id)

    def create_order(self, cart: UUID, price=float) -> Order:
        order = Order(id=uuid4(), cart=cart, discount=None, status=OrderStatuses.CREATED, price=price)
        return self.order_repo.create_order(order)

    def paid_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatuses.CREATED:
            raise ValueError
        order.status = OrderStatuses.PAID
        return self.order_repo.set_status(order)

    def set_discount(self, id: UUID, discount: float) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status == OrderStatuses.CREATED:
            order.discount = discount
            return self.order_repo.set_discount(order)
        raise ValueError

    def finish_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status == OrderStatuses.CREATED:
            raise ValueError
        order.status = OrderStatuses.DONE
        return self.order_repo.set_status(order)
    
    
    
        