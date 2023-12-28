from uuid import UUID
from app.models.promocode import Promocode
from fastapi import Depends


from app.repo.local_promocode_repo import PromocodeRepo


class PromocodeService():
    promocode_repo: PromocodeRepo

    def __init__(self, promocode_repo: PromocodeRepo = Depends(PromocodeRepo)) -> None:
        self.promocode_repo = promocode_repo
    
    def get_promocode(self, code: str) -> Promocode:
        return self.promocode_repo.get_promocode(code)
    
    def get_promocodes(self) -> list[Promocode]:
        return self.promocode_repo.get_promocodes()
    
    def create_promocode(self, code: str, discount: float) -> Promocode:
        return self.promocode_repo.create_promocode(code, discount)