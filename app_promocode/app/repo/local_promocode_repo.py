from uuid import UUID, uuid4

from app.models.promocode import Promocode
import logging

logging.basicConfig(level=logging.INFO)


promocodes: list[Promocode] = [
    Promocode(id=UUID('de2f3430-f54c-400b-954f-035ab10a4b84'),
              code="microservices2023",
              discount=0.10),
    Promocode(id=UUID('e7c5f6d3-a410-47c2-95bb-725d8403efb8'),
              code="IKBO-07-20",
              discount=0.20),
    Promocode(id=UUID('7e43fdaf-2bb6-41df-a1fb-c8d180704f62'),
              code="Skalozubov",
              discount=0.30),
]

class PromocodeRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            promocodes.clear()
    
    def get_promocodes(self) -> list[Promocode]:
        return promocodes

    def get_promocode(self, code: str) -> list[Promocode]:
        for p in promocodes:
            if p.code == code:
                return p.discount
        raise ValueError(f"Promocode with code '{code}' do not exists")
    
    def create_promocode(self, code: str, discount: float) -> Promocode:
        existing_promocode = next((p for p in promocodes if p.code == code), None)
        if existing_promocode:
            raise ValueError(f"Promocode with code '{code}' already exists")
        new_promocode = Promocode(id=uuid4(), code=code, discount=discount)
        promocodes.append(new_promocode)
        return new_promocode