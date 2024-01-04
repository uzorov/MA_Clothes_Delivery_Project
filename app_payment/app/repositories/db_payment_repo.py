import random
import traceback
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment_model import Payment
from app.schemas.payment_schema import Payment as DBPayment

class PaymentRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, payment: DBPayment) -> Payment:
        result = Payment.from_orm(payment)
        return result

    def _map_to_schema(self, payment: Payment) -> DBPayment:
        data = dict(payment)
        result = DBPayment(**data)
        return result

    def create_payment(self, payment: Payment) -> Payment:
        try:
            db_payment = self._map_to_schema(payment)
            self.db.add(db_payment)
            self.db.commit()
            return self._map_to_model(db_payment)
        except Exception as e:
            traceback.print_exc()
            self.db.rollback()
            raise e

    def get_all_payments(self) -> List[Payment]:
        payments = []
        for p in self.db.query(DBPayment).all():
            payments.append(self._map_to_model(p))
        return payments

    def get_user_payments(self, user_id: UUID) -> List[Payment]:
        payments = []
        for p in self.db.query(DBPayment).filter(DBPayment.user_id == user_id):
            payments.append(self._map_to_model(p))
        return payments

    def get_payment_by_id(self, payment_id: UUID) -> Payment:
        payment = self.db \
            .query(DBPayment) \
            .filter(DBPayment.id == payment_id) \
            .first()

        if payment is None:
            raise KeyError(f"Payment with id {payment_id} not found.")
        return self._map_to_model(payment)

    def process_payment(self, payment_id: UUID) -> str:
        try:
            payment = self.get_payment_by_id(payment_id)
            success = bool(random.getrandbits(1))
            return "Payment processed successfully" if success else "Payment failed"
        except KeyError:
            return "Payment not found"