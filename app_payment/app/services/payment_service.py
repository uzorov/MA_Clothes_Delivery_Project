from fastapi import Depends
from uuid import UUID, uuid4
from typing import List

from app.models.payment_model import Payment, PaymentType
from app.repositories.payment_repo import PaymentRepo


class PaymentService:
    payment_repo: PaymentRepo

    def __init__(self, payment_repo: PaymentRepo = Depends(PaymentRepo)) -> None:
        self.payment_repo = payment_repo

    def get_all_payments(self) -> List[Payment]:
        return self.payment_repo.get_all_payments()

    def create_payment(self, receiver: str, sum: int, payment_type: PaymentType) -> Payment:
        payment = Payment(id=uuid4(), receiver=receiver, sum=sum, type=payment_type)
        return self.payment_repo.create_payment(payment)

    def process_payment(self, payment_id: UUID) -> str:
        return self.payment_repo.process_payment(payment_id)

    def get_payment_by_id(self, payment_id: UUID) -> Payment:
        return self.payment_repo.get_payment_by_id(payment_id)
