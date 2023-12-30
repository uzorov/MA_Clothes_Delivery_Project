import random
from datetime import datetime, timedelta
from typing import List
from uuid import UUID
from app.models.payment_model import Payment

payments: List[Payment] = []


class PaymentRepo:

    def __init__(self, clear: bool = False) -> None:
        if clear:
            payments.clear()

    def create_payment(self, payment: Payment,) -> Payment:
        if len([p for p in payments if p.id == payment.id]) > 0:
            raise KeyError("Payment with the same id already exists.")

        payments.append(payment)
        return payment

    def get_all_payments(self) -> List[Payment]:
        return payments

    def get_payment_by_id(self, payment_id: UUID) -> Payment:
        for payment in payments:
            if payment.id == payment_id:
                return payment

        raise KeyError

    def get_user_payments(self, user_id: UUID) -> List[Payment]:
        user_payments = []
        for p in payments:
            if p.user_id == user_id:
                user_payments.append(p)
        return payments

    def process_payment(self, payment_id: UUID) -> str:
        try:
            payment = self.get_payment_by_id(payment_id)
            # Здесь вы можете добавить логику обработки оплаты, например, взаимодействие с платежным шлюзом.
            # Для примера, просто устанавливаем сообщение в зависимости от случайного значения.
            success = bool(random.getrandbits(1))
            return "Payment processed successfully" if success else "Payment failed"
        except KeyError:
            return "Payment not found"