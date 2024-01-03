from app.models.item import Item
from app.models.design import Design
from uuid import UUID, uuid4

# Добавить дизайны
designs = [
    Design(id=UUID('d2a103d0-2e8c-4d0e-9cf3-f85ac2da4eb2'), name='Design1', image_url='url1'),
    Design(id=UUID('f23e45f1-dfd3-4c08-a8a7-4cd0a0ddbf62'), name='Design2', image_url='url2'),
]

# Добавить элементы с дизайнами
items: list[Item] = [
    Item(id=UUID('de2f3430-f54c-400b-954f-035ab10a4b84'), name='Футболка1', price=500, design=designs[0]),
    Item(id=UUID('e7c5f6d3-a410-47c2-95bb-725d8403efb8'), name='Джинсы', price=3000, design=designs[1]),
    Item(id=UUID('7e43fdaf-2bb6-41df-a1fb-c8d180704f62'), name='Футболка2', price=700, design=designs[0]),
]


class ItemRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            items.clear()
    
    def get_items(self) -> list[Item]:
        return items

    def get_item(self, name: str) -> list[Item]:
        for i in items:
            if i.name == name:
                return i
        raise ValueError(f"Promocode with code '{name}' do not exists")
    
    def get_item_by_id(self, id: UUID) -> list[Item]:
        for i in items:
            if i.id == UUID(id):
                return i
        raise ValueError(f"Promocode with code '{id}' do not exists")
    
    def create_item(self, name: str, price: float) -> Item:
        existing_items = next((i for i in items if i.name == name), None)
        if existing_items:
            raise ValueError(f"Promocode with code '{name}' already exists")
        new_item = Item(id=uuid4(), name=name, price=price)
        items.append(new_item)
        return new_item
