import traceback
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item import Item
from app.schemas.item_schema import Item as DBItem


class ItemRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, item: DBItem) -> Item:
        result = Item.from_orm(item)
        return result

    def _map_to_schema(self, item: Item) -> DBItem:
        data = dict(item)
        result = DBItem(**data)
        return result

    def get_items(self) -> List[Item]:
        items = []
        for i in self.db.query(DBItem).all():
            items.append(self._map_to_model(i))
        return items

    def get_item_by_id(self, id: UUID) -> Item:
        item = self.db \
            .query(DBItem) \
            .filter(DBItem.id == id) \
            .first()

        if item is None:
            raise KeyError(f"Item with id {id} not found.")
        return self._map_to_model(item)

    def create_item(self, item: Item) -> Item:
        try:
            db_item = self._map_to_schema(item)
            self.db.add(db_item)
            self.db.commit()
            return self._map_to_model(db_item)
        except Exception as e:
            traceback.print_exc()
            self.db.rollback()
            raise e

    def update_price(self, item: Item) -> Item:
        db_item = self.db.query(DBItem).filter(
            DBItem.id == item.id).first()
        db_item.price = item.price
        self.db.commit()
        return self._map_to_model(db_item)

    def update_design(self, item: Item) -> Item:
        db_item = self.db.query(DBItem).filter(
            DBItem.id == item.id).first()
        db_item.design = item.design
        self.db.commit()
        return self._map_to_model(db_item)

    def delete_item(self, item_id: UUID) -> Item:
        db_item = self.db.query(DBItem).filter(
            DBItem.id == item_id).first()

        if db_item is None:
            raise KeyError(f"Item with id {item_id} not found.")

        deleted_item = self._map_to_model(db_item)
        self.db.delete(db_item)
        self.db.commit()
        return deleted_item
