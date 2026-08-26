from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.existing.loan import Loan
from app.schemas.loan import UserRequest
from app.models.existing.loan_payment import LoanPayment


router = APIRouter()


@router.post("")
def get_loans(
    request: UserRequest,
    db: Session = Depends(get_db),
):
    loans = (
        db.query(Loan)
        .filter(Loan.customer_id == request.user_id)
        .all()
    )

    return {
        "user_id": request.user_id,
        "total_loans": len(loans),
        "loans": loans,
    }

@router.post("/history")
def get_loan_history(
    request: UserRequest,
    db: Session = Depends(get_db),
):
    loans = (
        db.query(Loan)
        .filter(Loan.customer_id == request.user_id)
        .all()
    )

    if not loans:
        return {
            "user_id": request.user_id,
            "total_loans": 0,
            "loan_history": [],
        }

    loan_ids = [loan.id for loan in loans]

    payments = (
        db.query(LoanPayment)
        .filter(LoanPayment.loan_id.in_(loan_ids))
        .order_by(LoanPayment.payment_date.desc())
        .all()
    )

    return {
        "user_id": request.user_id,
        "total_payments": len(payments),
        "loan_history": payments,
    }