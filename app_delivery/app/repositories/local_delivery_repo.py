# /app/repositories/local_delivery_repo.py

from uuid import UUID

from app.models.delivery import Delivery


deliveries: list[Delivery] = []


class DeliveryRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            deliveries.clear()

    def get_deliveries(self) -> list[Delivery]:
        return deliveries

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        for d in deliveries:
            if d.id == id:
                return d

        raise KeyError

    def create_delivery(self, delivery: Delivery) -> Delivery:
        if len([d for d in deliveries if d.id == delivery.id]) > 0:
            raise KeyError

        deliveries.append(delivery)
        return delivery

    def set_status(self, delivery: Delivery) -> Delivery:
        for d in deliveries:
            if d.id == delivery.id:
                d.status = delivery.status
                break

        return delivery

    def set_type(self, delivery: Delivery) -> Delivery:
        for d in deliveries:
            if d.id == delivery.id:
                d.type = delivery.type
                break

        return delivery
