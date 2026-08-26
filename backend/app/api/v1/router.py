from fastapi import APIRouter

from app.api.v1 import transactions
from app.api.v1 import loans
from app.api.v1 import accounts


api_router = APIRouter()

api_router.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transactions"],
)

api_router.include_router(
    loans.router,
    prefix="/loans",
    tags=["Loans"],
)

api_router.include_router(
    accounts.router,
    prefix="/accounts",
    tags=["Accounts"],
)