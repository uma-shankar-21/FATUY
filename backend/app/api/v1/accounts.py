from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.existing.bank_account import BankAccount
from app.schemas.account import AccountBalanceRequest


router = APIRouter()


@router.post("/balance")
def get_account_balance(
    request: AccountBalanceRequest,
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

    total_balance = sum(
        account.balance for account in accounts
    )

    return {
        "user_id": request.user_id,
        "total_balance": total_balance,
        "accounts": accounts,
    }