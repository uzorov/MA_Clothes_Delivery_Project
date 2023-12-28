# /app_printing/repositories/local_printing_repo.py

from uuid import UUID

from app.models.printing import Printing


printings: list[Printing] = []


class PrintingRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            printings.clear()

    def get_printings(self) -> list[Printing]:
        return printings

    def get_printing_by_id(self, id: UUID) -> Printing:
        for p in printings:
            if p.id == id:
                return p

        raise KeyError

    def create_printing(self, printing: Printing) -> Printing:
        if len([p for p in printings if p.id == printing.id]) > 0:
            raise KeyError

        printings.append(printing)
        return printing

    def set_status(self, printing: Printing) -> Printing:
        for p in printings:
            if p.id == printing.id:
                p.status = printing.status
                break
        return printing
