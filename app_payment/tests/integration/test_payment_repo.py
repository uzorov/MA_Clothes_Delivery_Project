import pytest
from uuid import UUID,uuid4
from app.models.payment_model import Payment
from app.repositories.db_payment_repo import PaymentRepo

@pytest.fixture()
def payment_repo() -> PaymentRepo:
    repo = PaymentRepo()
    return repo

@pytest.fixture(scope='session')
def sample_payment() -> Payment:
    return Payment(
        id=uuid4(),
        receiver='John Doe',
        sum=100,
        user_id=uuid4(),
        order_id=uuid4()
    )

def test_create_payment(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    assert payment_repo.create_payment(sample_payment) == sample_payment

def test_get_payment_by_id(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    retrieved_payment = payment_repo.get_payment_by_id(sample_payment.id)
    assert retrieved_payment == sample_payment

def test_process_payment(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    result = payment_repo.process_payment(sample_payment.id)
    assert result in ["Payment processed successfully", "Payment failed"]

def test_get_all_payments(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    payments = payment_repo.get_all_payments()
    assert sample_payment in payments


