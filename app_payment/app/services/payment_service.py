from fastapi import Depends
from uuid import UUID, uuid4
from typing import List

from app.models.payment_model import Payment
from app.repositories.db_payment_repo import PaymentRepo


class PaymentService:
    payment_repo: PaymentRepo

    def __init__(self, payment_repo: PaymentRepo = Depends(PaymentRepo)) -> None:
        self.payment_repo = payment_repo

    def get_all_payments(self) -> List[Payment]:
        return self.payment_repo.get_all_payments()

    def get_user_payments(self, user_id: UUID) -> List[Payment]:
        return self.payment_repo.get_user_payments(user_id)

    def create_payment(self, sum: int, user_id: UUID,order_id: UUID) -> Payment:
        receiver = "ООО Зеленоглазое такси"
        payment = Payment(id=uuid4(), user_id=user_id, receiver=receiver, sum=sum, order_id=order_id)
        return self.payment_repo.create_payment(payment)

    def process_payment(self, payment_id: UUID) -> str:
        return self.payment_repo.process_payment(payment_id)

    def get_payment_by_id(self, payment_id: UUID) -> Payment:
        return self.payment_repo.get_payment_by_id(payment_id)
