# /app/services/delivery_service.py

from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatuses, DeliveryTypes
from app.repositories.db_delivery_repo import DeliveryRepo


class DeliveryService():
    delivery_repo: DeliveryRepo

    def __init__(self, delivery_repo: DeliveryRepo = Depends(DeliveryRepo)) -> None:
        self.delivery_repo = delivery_repo

    def get_deliveries(self) -> list[Delivery]:
        return self.delivery_repo.get_deliveries()

    def get_delivery_by_id(self, id: UUID) -> list[Delivery]:
        return self.delivery_repo.get_delivery_by_id(id)

    def create_delivery(self, id: UUID) -> Delivery:  # , date: datetime, address: str
        delivery = Delivery(
            id=id,
            address="To Be Chosen",
            date="2000-01-01 00:00:00.000",
            status=DeliveryStatuses.CREATED,
            type=DeliveryTypes.PICKUP)
        return self.delivery_repo.create_delivery(delivery)

    def activate_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status != DeliveryStatuses.CREATED:
            raise ValueError

        delivery.status = DeliveryStatuses.IN_PROCESS
        return self.delivery_repo.set_status(delivery)

    def finish_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status != DeliveryStatuses.IN_PROCESS:
            raise ValueError

        delivery.status = DeliveryStatuses.DONE
        return self.delivery_repo.set_status(delivery)

    def cancel_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.status == DeliveryStatuses.DONE:
            raise ValueError

        delivery.status = DeliveryStatuses.CANCELED
        return self.delivery_repo.set_status(delivery)

    def choose_pickup(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.type == DeliveryTypes.PICKUP:
            raise ValueError

        delivery.type = DeliveryTypes.PICKUP
        return self.delivery_repo.set_type(delivery)

    def choose_delivery(self, id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(id)
        if delivery.type == DeliveryTypes.DELIVERY:
            raise ValueError

        delivery.type = DeliveryTypes.DELIVERY
        return self.delivery_repo.set_type(delivery)
