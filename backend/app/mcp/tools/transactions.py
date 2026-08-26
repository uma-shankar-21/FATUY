import httpx

from app.core.config import settings
from app.mcp.schemas import MCPToolResult


async def get_transactions(
    user_id: str,
    transaction_type: str | None = None,
    amount: float | None = None,
    description: str | None = None,
    merchant: str | None = None,
    category: str | None = None,
    status: str | None = None,
    transaction_date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: str | None = None,
) -> MCPToolResult:

    cleaned_limit = None
    if limit is not None and str(limit).strip() != "":
        try:
            cleaned_limit = int(limit)
        except (TypeError, ValueError):
            cleaned_limit = None

    payload = {
        "user_id": user_id,
        "transaction_type": transaction_type,
        "amount": amount,
        "description": description,
        "merchant": merchant,
        "category": category,
        "status": status,
        "transaction_date": transaction_date,
        "start_date": start_date,
        "end_date": end_date,
        "limit": cleaned_limit,
    }

    payload = {
        key: value
        for key, value in payload.items()
        if value not in (None, "", [])
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:

            response = await client.post(
                f"{settings.MCP_API_BASE_URL}/transactions/search",
                json=payload,
            )

            response.raise_for_status()

            return MCPToolResult(
                success=True,
                tool_name="get_transactions",
                data=response.json(),
            )

    except httpx.HTTPError as error:

        return MCPToolResult(
            success=False,
            tool_name="get_transactions",
            error=str(error),
        )