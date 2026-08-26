from app.mcp.tools.transactions import get_transactions
from app.mcp.tools.loans import get_loans
from app.mcp.tools.loan_history import get_loan_history
from app.mcp.tools.accounts import get_account_balance


MCP_TOOLS = {
    "get_transactions": get_transactions,
    "get_loans": get_loans,
    "get_loan_history": get_loan_history,
    "get_account_balance": get_account_balance,
}