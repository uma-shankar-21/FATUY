import httpx

from app.core.config import settings
from app.mcp.schemas import MCPToolResult


async def get_account_balance(
    user_id: str,
) -> MCPToolResult:

    payload = {
        "user_id": user_id,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:

            response = await client.post(
                f"{settings.MCP_API_BASE_URL}/accounts/balance",
                json=payload,
            )

            response.raise_for_status()

            return MCPToolResult(
                success=True,
                tool_name="get_account_balance",
                data=response.json(),
            )

    except httpx.HTTPError as error:

        return MCPToolResult(
            success=False,
            tool_name="get_account_balance",
            error=str(error),
        )