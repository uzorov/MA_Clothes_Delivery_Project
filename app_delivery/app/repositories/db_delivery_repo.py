# /app/repositories/bd_delivery_repo.py

import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.delivery import Delivery
from app.schemas.delivery import Delivery as DBDelivery


class DeliveryRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, delivery: DBDelivery) -> Delivery:
        result = Delivery.from_orm(delivery)
        return result

    def _map_to_schema(self, delivery: Delivery) -> DBDelivery:
        data = dict(delivery)
        result = DBDelivery(**data)
        return result
    
    def get_delivery_by_id(self, id: UUID) -> Delivery:
        return self.db.query(DBDelivery).filter(DBDelivery.id == id).first()

    def get_deliveries(self) -> list[Delivery]:
        deliveries = []
        for d in self.db.query(DBDelivery).all():
            deliveries.append(self._map_to_model(d))
        return deliveries

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        delivery = self.db \
            .query(DBDelivery) \
            .filter(DBDelivery.id == id) \
            .first()

        if delivery == None:
            raise KeyError
        return self._map_to_model(delivery)

    def create_delivery(self, delivery: Delivery) -> Delivery:
        try:
            db_delivery = self._map_to_schema(delivery)
            self.db.add(db_delivery)
            self.db.commit()
            return self._map_to_model(db_delivery)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, delivery: Delivery) -> Delivery:
        db_delivery = self.db.query(DBDelivery).filter(
            DBDelivery.id == delivery.id).first()
        db_delivery.status = delivery.status
        self.db.commit()
        return self._map_to_model(db_delivery)

    def set_type(self, delivery: Delivery) -> Delivery:
        db_delivery = self.db.query(DBDelivery).filter(
            DBDelivery.id == delivery.id).first()
        db_delivery.type = delivery.type
        self.db.commit()
        return self._map_to_model(db_delivery)

    def delete_all_deliveries(self) -> None:
        self.db.query(DBDelivery).delete()
        self.db.commit()
