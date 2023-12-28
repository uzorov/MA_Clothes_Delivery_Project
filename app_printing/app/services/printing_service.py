# /app_printing/services/printing_service.py
import asyncio
from datetime import datetime
from uuid import UUID

from app.models.printing import Printing, PrintingStatuses
from app.repositories.db_printing_repo import PrintingRepo
from fastapi import Depends
from app.printing_finished_trigger import run_main, get_id


class PrintingService():
    printing_repo: PrintingRepo

    def __init__(self, printing_repo: PrintingRepo = Depends(PrintingRepo)) -> None:
        self.printing_repo = printing_repo

    def get_printings(self) -> list[Printing]:
        return self.printing_repo.get_printings()

    def create_printing(self, order_id: UUID, date: datetime) -> Printing:
        printing = Printing(id=order_id, date=date, status=PrintingStatuses.AWAITING)
        return self.printing_repo.create_printing(printing)

    def begin_printing(self, id: UUID) -> Printing:
        printing = self.printing_repo.get_printing_by_id(id)
        if printing.status != PrintingStatuses.AWAITING:
            raise ValueError

        printing.status = PrintingStatuses.IN_PROCESS
        return self.printing_repo.set_status(printing)

    def finish_printing(self, id: UUID) -> Printing:
        printing = self.printing_repo.get_printing_by_id(id)
        if printing.status != PrintingStatuses.IN_PROCESS:
            raise ValueError

        printing.status = PrintingStatuses.DONE
        get_id(id)
        run_main(id)
        return self.printing_repo.set_status(printing)

    def cancel_printing(self, id: UUID) -> Printing:
        printing = self.printing_repo.get_printing_by_id(id)
        if printing.status == PrintingStatuses.DONE:
            raise ValueError

        printing.status = PrintingStatuses.CANCELED
        return self.printing_repo.set_status(printing)
        