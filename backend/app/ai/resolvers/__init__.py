from app.ai.resolvers.accounts import AccountResolver
from app.ai.resolvers.loan_history import LoanHistoryResolver
from app.ai.resolvers.loans import LoansResolver
from app.ai.resolvers.transactions import TransactionsResolver


RESOLVERS = {
    "transactions": TransactionsResolver(),
    "loans": LoansResolver(),
    "loan_history": LoanHistoryResolver(),
    "account_balance": AccountResolver(),
}


def get_resolver(
    resource: str,
):

    resolver = RESOLVERS.get(resource)

    if not resolver:
        raise ValueError(
            f"Unknown resource: {resource}"
        )

    return resolver