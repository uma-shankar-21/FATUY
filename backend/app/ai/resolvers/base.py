from abc import ABC, abstractmethod
from typing import Any


class BaseResolver(ABC):

    @abstractmethod
    async def resolve(
        self,
        user_id: str,
        filters: dict[str, Any],
    ) -> Any:
        pass