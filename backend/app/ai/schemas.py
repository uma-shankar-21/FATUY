from typing import Any, Literal

from pydantic import BaseModel, Field


class AIRequestPlan(BaseModel):

    resource: Literal[
        "transactions",
        "loans",
        "loan_history",
        "account_balance",
    ]

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )

    required_fields: list[str] = Field(
        default_factory=list,
    )