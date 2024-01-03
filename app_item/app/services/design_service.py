from fastapi import Depends
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

from app.models.design import Design
from app.repositories.design_repo import DesignRepo


class DesignService:
    design_repo: DesignRepo

    def __init__(self, design_repo: DesignRepo = Depends(DesignRepo)) -> None:
        self.design_repo = design_repo

    def create_design(self,image_url: str) -> Design:
        design = Design(id=uuid4(), image_url=image_url)
        return self.design_repo.create_design(design)

    def update_design_image(self, design_id: UUID, new_image: str) -> Design:
        design = self.design_repo.get_design_by_id(design_id)
        design.image_url = new_image
        return self.design_repo.set_image(design)

    def delete_design(self, design_id: UUID) -> Design:
        return self.design_repo.delete_design(design_id)

    def get_design_by_id(self, design_id: UUID) -> Design:
        return self.design_repo.get_design_by_id(design_id)
