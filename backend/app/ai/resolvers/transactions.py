import httpx

from app.ai.resolvers.base import BaseResolver
from app.core.config import settings


class TransactionsResolver(BaseResolver):

    async def resolve(
        self,
        user_id: str,
        filters: dict,
    ):

        payload = {
            "user_id": user_id,
            **filters,
        }

        payload = {
            key: value
            for key, value in payload.items()
            if value is not None
        }

        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:

            response = await client.post(
                f"{settings.MCP_API_BASE_URL}/transactions/search",
                json=payload,
            )

            response.raise_for_status()

            return response.json()