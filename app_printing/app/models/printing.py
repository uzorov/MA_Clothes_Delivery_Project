# /app_printing/models/printing.py

from __future__ import annotations

import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PrintingStatuses(enum.Enum):
    AWAITING = 'awaiting'
    IN_PROCESS = 'in_process'
    DONE = 'done'
    CANCELED = 'canceled'


class Printing(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date: datetime
    status: PrintingStatuses


class CreatePrintingRequest(BaseModel):
    id: UUID
