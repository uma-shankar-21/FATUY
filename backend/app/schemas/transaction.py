from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, model_validator


class TransactionSearchRequest(BaseModel):
    user_id: str

    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    merchant: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None

    transaction_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.transaction_date and (
            self.start_date or self.end_date
        ):
            raise ValueError(
                "Use either transaction_date OR start_date/end_date, not both."
            )

        if self.start_date and not self.end_date:
            raise ValueError(
                "end_date is required when start_date is provided."
            )

        if self.end_date and not self.start_date:
            raise ValueError(
                "start_date is required when end_date is provided."
            )

        if (
            self.start_date
            and self.end_date
            and self.start_date > self.end_date
        ):
            raise ValueError(
                "start_date cannot be greater than end_date."
            )

        return self