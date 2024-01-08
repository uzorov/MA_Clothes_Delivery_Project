# /app_printing/repositories/db_printing_repo.py
import traceback
from uuid import UUID

from app.database import get_db
from app.models.printing import Printing
from app.schemas.printing import Printing as DBPrinting
from sqlalchemy.orm import Session


class PrintingRepo():
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, printing: DBPrinting) -> Printing:
        result = Printing.from_orm(printing)
        return result

    def _map_to_schema(self, printing: Printing) -> DBPrinting:
        data = dict(printing)
        result = DBPrinting(**data)
        return result

    def get_printings(self) -> list[Printing]:
        printings = []
        for p in self.db.query(DBPrinting).all():
            printings.append(self._map_to_model(p))
        return printings

    def get_printing_by_id(self, id: UUID) -> Printing:
        printing = self.db \
            .query(DBPrinting) \
            .filter(DBPrinting.id == id) \
            .first()

        if printing == None:
            raise None
        return self._map_to_model(printing)

    def create_printing(self, printing: Printing) -> Printing:
        try:
            db_printing = self._map_to_schema(printing)
            self.db.add(db_printing)
            self.db.commit()
            return self._map_to_model(db_printing)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, printing: Printing) -> Printing:
        db_printing = self.db.query(DBPrinting).filter(
            DBPrinting.id == printing.id).first()
        db_printing.status = printing.status
        self.db.commit()
        return self._map_to_model(db_printing)

    def delete_all_printings(self) -> None:
        self.db.query(DBPrinting).delete()
        self.db.commit()