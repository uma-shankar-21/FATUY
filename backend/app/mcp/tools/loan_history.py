import httpx

from app.core.config import settings
from app.mcp.schemas import MCPToolResult


async def get_loan_history(
    user_id: str,
) -> MCPToolResult:

    payload = {
        "user_id": user_id,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:

            response = await client.post(
                f"{settings.MCP_API_BASE_URL}/loans/history",
                json=payload,
            )

            response.raise_for_status()

            return MCPToolResult(
                success=True,
                tool_name="get_loan_history",
                data=response.json(),
            )

    except httpx.HTTPError as error:

        return MCPToolResult(
            success=False,
            tool_name="get_loan_history",
            error=str(error),
        )