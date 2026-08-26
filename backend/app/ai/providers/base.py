from abc import ABC, abstractmethod
from typing import Any


class BaseAIProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        pass