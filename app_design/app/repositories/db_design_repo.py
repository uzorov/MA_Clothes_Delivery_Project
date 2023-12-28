import traceback
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.design_model import Design
from app.schemas.design_schema import Design as DBDesign


class DesignRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, design: DBDesign) -> Design:
        result = Design.from_orm(design)
        return result

    def _map_to_schema(self, design: Design) -> DBDesign:
        data = dict(design)
        result = DBDesign(**data)
        return result

    def get_designs(self) -> List[Design]:
        designs = []
        for d in self.db.query(DBDesign).all():
            designs.append(self._map_to_model(d))
        return designs

    def get_design_by_id(self, id: UUID) -> Design:
        design = self.db \
            .query(DBDesign) \
            .filter(DBDesign.id == id) \
            .first()

        if design is None:
            raise KeyError(f"Design with id {id} not found.")
        return self._map_to_model(design)

    def create_design(self, design: Design) -> Design:
        try:
            db_design = self._map_to_schema(design)
            self.db.add(db_design)
            self.db.commit()
            return self._map_to_model(db_design)
        except Exception as e:
            traceback.print_exc()
            self.db.rollback()
            raise e

    def set_status(self, design: Design) -> Design:
        db_design = self.db.query(DBDesign).filter(
            DBDesign.id == design.id).first()
        db_design.status = design.status
        self.db.commit()
        return self._map_to_model(db_design)

    def set_image(self, design: Design) -> Design:
        db_design = self.db.query(DBDesign).filter(
            DBDesign.id == design.id).first()
        db_design.image_url = design.image_url
        self.db.commit()
        return self._map_to_model(db_design)

    def delete_design(self, design_id: UUID) -> Design:
        db_design = self.db.query(DBDesign).filter(
            DBDesign.id == design_id).first()

        if db_design is None:
            raise KeyError(f"Design with id {design_id} not found.")

        deleted_design = self._map_to_model(db_design)
        self.db.delete(db_design)
        self.db.commit()
        return deleted_design