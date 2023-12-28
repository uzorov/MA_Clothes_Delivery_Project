from fastapi import Depends
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

from app.models.design_model import Design, DesignStatuses
from app.repositories.design_repo import DesignRepo


class DesignService:
    design_repo: DesignRepo

    def __init__(self, design_repo: DesignRepo = Depends(DesignRepo)) -> None:
        self.design_repo = design_repo

    def get_designs(self) -> List[Design]:
        return self.design_repo.get_designs()

    def create_design(self, name:str, image_url: str) -> Design:
        if not name and not image_url:
            name = 'Пустой дизайн'
        elif not name:
            name = 'Свой дизайн'
        design = Design(id=uuid4(), name = name, image_url=image_url, status=DesignStatuses.AVAILABLE)
        return self.design_repo.create_design(design)

    def update_design_status(self, design_id: UUID, new_status: DesignStatuses) -> Design:
        design = self.design_repo.get_design_by_id(design_id)
        design.status = new_status
        return self.design_repo.set_status(design)

    def update_design_image(self, design_id: UUID, new_image: str) -> Design:
        design = self.design_repo.get_design_by_id(design_id)
        design.image_url = new_image
        return self.design_repo.set_image(design)

    def delete_design(self, design_id: UUID) -> Design:
        return self.design_repo.delete_design(design_id)

    def get_design_by_id(self, design_id: UUID) -> Design:
        return self.design_repo.get_design_by_id(design_id)
