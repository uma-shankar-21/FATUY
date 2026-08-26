from datetime import datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.existing.bank_account import BankAccount
from app.models.existing.transaction import Transaction
from app.schemas.transaction import TransactionSearchRequest


router = APIRouter()


@router.post("/search")
def get_transactions(
    request: TransactionSearchRequest,
    db: Session = Depends(get_db),
):
    accounts = (
        db.query(BankAccount)
        .filter(BankAccount.customer_id == request.user_id)
        .all()
    )

    if not accounts:
        raise HTTPException(
            status_code=404,
            detail="No bank accounts found for this user.",
        )

    account_ids = [account.id for account in accounts]

    query = db.query(Transaction).filter(
        Transaction.account_id.in_(account_ids)
    )

    if request.transaction_type:
        query = query.filter(
            Transaction.transaction_type == request.transaction_type
        )

    if request.amount is not None:
        query = query.filter(
            Transaction.amount == request.amount
        )

    if request.description:
        query = query.filter(
            Transaction.description.ilike(
                f"%{request.description}%"
            )
        )

    if request.merchant:
        query = query.filter(
            Transaction.merchant.ilike(
                f"%{request.merchant}%"
            )
        )

    if request.category:
        query = query.filter(
            Transaction.category.ilike(
                f"%{request.category}%"
            )
        )

    if request.status:
        query = query.filter(
            Transaction.status == request.status
        )

    # Single date
    if request.transaction_date:
        start_datetime = datetime.combine(
            request.transaction_date,
            time.min,
        )

        end_datetime = datetime.combine(
            request.transaction_date,
            time.max,
        )

        query = query.filter(
            Transaction.transaction_date >= start_datetime,
            Transaction.transaction_date <= end_datetime,
        )

    # Date range
    if request.start_date and request.end_date:
        start_datetime = datetime.combine(
            request.start_date,
            time.min,
        )

        end_datetime = datetime.combine(
            request.end_date,
            time.max,
        )

        query = query.filter(
            Transaction.transaction_date >= start_datetime,
            Transaction.transaction_date <= end_datetime,
        )

    transactions = (
        query
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    return {
        "user_id": request.user_id,
        "total_transactions": len(transactions),
        "transactions": transactions,
    }