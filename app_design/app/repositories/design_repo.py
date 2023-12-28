from datetime import datetime, timedelta
from typing import List
from uuid import UUID
from app.models.design_model import Design, DesignStatuses

designs: list[Design] = [
    Design(id=UUID('16d74d90-6e38-4bd4-be00-8e0e271f9351'),
           name='Крутой перец',
           image_url='https://example.com/design1.jpg',
           status=DesignStatuses.AVAILABLE),
    Design(id=UUID('cb778c3b-a9ae-42e1-9300-e32c062aaec2'),
           name='Память Бориса',
           image_url='https://example.com/design2.jpg',
           status=DesignStatuses.UNAVAILABLE),
    Design(id=UUID('ebb0f5a1-5e6c-4c20-8e97-950f11263a82'),
           name='Ласковая кошечка',
           image_url='https://example.com/design3.jpg',
           status=DesignStatuses.AVAILABLE),
    Design(id=UUID('79806030-5181-45ee-b760-111409f874a9'),
           name='Варяг',
           image_url='https://example.com/design4.jpg',
           status=DesignStatuses.UNAVAILABLE),
    Design(id=UUID('d6524ca2-a122-4d58-aa75-1079688a9922'),
           name='Самый крутой батя',
           image_url='https://example.com/design5.jpg',
           status=DesignStatuses.AVAILABLE)
]


class DesignRepo:

    def __init__(self, clear: bool = False) -> None:
        if clear:
            designs.clear()

    def get_designs(self) -> List[Design]:
        return designs

    def get_design_by_id(self, id: UUID) -> Design:
        for design in designs:
            if design.id == id:
                return design

        raise KeyError

    def create_design(self, design: Design) -> Design:
        if len([d for d in designs if d.id == design.id]) > 0:
            raise KeyError("Design with the same id already exists.")

        designs.append(design)
        return design

    def set_status(self, design: Design) -> Design:
        for d in designs:
            if d.id == design.id:
                d.status = design.status
                break

        return design

    def set_image(self, design: Design) -> Design:
        for d in designs:
            if d.id == design.id:
                d.image_url = design.image_url
                break

        return design

    def delete_design(self, design_id: UUID) -> Design:
        for i, design in enumerate(designs):
            if design.id == design_id:
                deleted_design = designs.pop(i)
                return deleted_design

        raise KeyError
