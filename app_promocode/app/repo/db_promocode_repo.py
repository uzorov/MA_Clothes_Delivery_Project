# /app_pomocode/repositories/db_promocode_repo.py
from uuid import UUID

from app.models.promocode import Promocode
from app.schemas.promocode import Promocode as DBPromocode
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import traceback

from app.database import get_db


class PromocodeRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, promocode: DBPromocode) -> Promocode:
        result = Promocode.from_orm(promocode)
        return result

    def _map_to_schema(self, promocode: Promocode) -> DBPromocode:
        data = dict(promocode)
        result = DBPromocode(**data)
        return result

    def get_promocodes(self) -> List[Promocode]:
        promocodes = []
        for p in self.db.query(DBPromocode).all():
            promocodes.append(self._map_to_model(p))
        return promocodes


    def create_promocode(self, code: str, discount: float) -> Promocode:
        try:
            db_promocode = self._map_to_schema(Promocode(code=code, discount=discount))
            self.db.add(db_promocode)
            self.db.commit()
            return self._map_to_model(db_promocode)
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Promocode with code '{code}' already exists") from e
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise e

