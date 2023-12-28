# tests/unit/test_payment_service.py
import pytest
from uuid import uuid4, UUID
from app.services.payment_service import PaymentService
from app.models.payment_model import Payment, PaymentType
from app.repositories.payment_repo import PaymentRepo

@pytest.fixture(scope='session')
def payment_service() -> PaymentService:
    return PaymentService(PaymentRepo(clear=True))

@pytest.fixture()
def payment_data() -> Payment:
    return Payment(
        id=uuid4(),
        receiver='John Doe',
        sum=100,
        type=PaymentType.PC
    )

def test_empty_payments(payment_service: PaymentService) -> None:
    assert payment_service.get_all_payments() == []

def test_create_payment(
        payment_data: Payment,
        payment_service: PaymentService
) -> None:
    payment = payment_service.create_payment(payment_data.receiver, payment_data.sum, payment_data.type)

    assert payment.receiver == payment_data.receiver
    assert payment.sum == payment_data.sum
    assert payment.type == payment_data.type

def test_process_payment(
        payment_data: Payment,
        payment_service: PaymentService
) -> None:
    payments = payment_service.get_all_payments()
    payment_data = payments[0]
    result = payment_service.process_payment(payment_data.id)
    assert result in ["Payment processed successfully", "Payment failed"]

def test_get_payment_by_id(
        payment_data: Payment,
        payment_service: PaymentService
) -> None:
    payment = payment_service.create_payment(payment_data.receiver, payment_data.sum, payment_data.type)
    payments = payment_service.get_all_payments()
    payment_data = payments[0]
    payment = payment_service.get_payment_by_id(payment_data.id)
    assert payment.id == payment_data.id
    assert payment.receiver == payment_data.receiver
    assert payment.sum == payment_data.sum
    assert payment.type == payment_data.type
