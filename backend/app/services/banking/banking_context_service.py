from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.existing.bank_account import BankAccount
from app.models.existing.transaction import Transaction
from app.models.existing.loan import Loan
from app.models.existing.loan_payment import LoanPayment


class BankingContextService:

    async def get_accounts(
        self,
        db: AsyncSession,
        user_id,
    ) -> list[dict]:

        result = await db.execute(
            select(BankAccount)
            .where(
                BankAccount.customer_id == user_id
            )
        )

        accounts = result.scalars().all()

        return [
            {
                "id": str(account.id),
                "account_number": account.account_number,
                "account_type": account.account_type,
                "currency": account.currency,
                "balance": float(account.balance),
                "status": account.status,
            }
            for account in accounts
        ]


    async def get_recent_transactions(
        self,
        db: AsyncSession,
        user_id,
        limit: int = 10,
    ) -> list[dict]:

        result = await db.execute(
            select(Transaction)
            .join(
                BankAccount,
                Transaction.account_id == BankAccount.id,
            )
            .where(
                BankAccount.customer_id == user_id
            )
            .order_by(
                Transaction.transaction_date.desc()
            )
            .limit(limit)
        )

        transactions = result.scalars().all()

        return [
            {
                "id": str(transaction.id),
                "account_id": str(transaction.account_id),
                "transaction_type": transaction.transaction_type,
                "amount": float(transaction.amount),
                "currency": transaction.currency,
                "description": transaction.description,
                "merchant": transaction.merchant,
                "transaction_date": str(
                    transaction.transaction_date
                ),
                "category": transaction.category,
                "status": transaction.status,
            }
            for transaction in transactions
        ]


    async def get_loans(
        self,
        db: AsyncSession,
        user_id,
    ) -> list[dict]:

        result = await db.execute(
            select(Loan)
            .where(
                Loan.customer_id == user_id
            )
        )

        loans = result.scalars().all()

        return [
            {
                "id": str(loan.id),
                "loan_type": loan.loan_type,
                "principal_amount": float(
                    loan.principal_amount
                ),
                "outstanding_amount": float(
                    loan.outstanding_amount
                ),
                "interest_rate": float(
                    loan.interest_rate
                ),
                "monthly_emi": float(
                    loan.monthly_emi
                ),
                "tenure_years": loan.tenure_years,
                "next_due_date": (
                    str(loan.next_due_date)
                    if loan.next_due_date
                    else None
                ),
                "status": loan.status,
            }
            for loan in loans
        ]


    async def get_recent_loan_payments(
        self,
        db: AsyncSession,
        user_id,
        limit: int = 10,
    ) -> list[dict]:

        result = await db.execute(
            select(LoanPayment)
            .join(
                Loan,
                LoanPayment.loan_id == Loan.id,
            )
            .where(
                Loan.customer_id == user_id
            )
            .order_by(
                LoanPayment.payment_date.desc()
            )
            .limit(limit)
        )

        payments = result.scalars().all()

        return [
            {
                "id": str(payment.id),
                "loan_id": str(payment.loan_id),
                "amount": float(payment.amount),
                "payment_date": str(
                    payment.payment_date
                ),
                "payment_number": payment.payment_number,
            }
            for payment in payments
        ]


banking_context_service = BankingContextService()