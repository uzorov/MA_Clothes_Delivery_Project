from uuid import UUID, uuid4
from app.models.item import Item
from fastapi import Depends
from app.models.item import Design

from app.repositories.db_item_repo import ItemRepo


class ItemService():
    item_repo: ItemRepo

    def __init__(self, item_repo: ItemRepo = Depends(ItemRepo)) -> None:
        self.item_repo = item_repo

    def get_item(self, name: str) -> Item:
        return self.item_repo.get_item(name)

    def get_items_by_id(self, id: UUID) -> Item:
        return self.item_repo.get_item_by_id(id)

    def get_items(self) -> list[Item]:
        return self.item_repo.get_items()

    def create_item(self, name: str, price: float, design: str) -> Item:
        if not name and not design:
            name = 'Пустой дизайн'
        elif not name:
            name = 'Свой дизайн'
        item = Item(id=uuid4(), name=name, price=price, design=design)
        return self.item_repo.create_item(item)
