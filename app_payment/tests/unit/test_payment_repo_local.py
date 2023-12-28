import pytest
from uuid import UUID, uuid4
from app.models.payment_model import Payment, PaymentType
from app.repositories.payment_repo import PaymentRepo

@pytest.fixture(scope='session')
def payment_repo() -> PaymentRepo:
    return PaymentRepo(clear=True)

@pytest.fixture(scope='session')
def sample_payment() -> Payment:
    return Payment(
        id=uuid4(),
        receiver='John Doe',
        sum=100,
        type=PaymentType.PC
    )


def test_create_payment(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    created_payment = payment_repo.create_payment(sample_payment)
    assert created_payment == sample_payment

def test_create_payment_duplicate(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    with pytest.raises(KeyError):
        payment_repo.create_payment(sample_payment)

def test_get_payment_by_id(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    retrieved_payment = payment_repo.get_payment_by_id(sample_payment.id)
    assert retrieved_payment == sample_payment

def test_get_payment_by_id_error(payment_repo: PaymentRepo) -> None:
    with pytest.raises(KeyError):
        payment_repo.get_payment_by_id(uuid4())

def test_process_payment(payment_repo: PaymentRepo, sample_payment: Payment) -> None:
    result = payment_repo.process_payment(sample_payment.id)
    assert result in ["Payment processed successfully", "Payment failed"]
