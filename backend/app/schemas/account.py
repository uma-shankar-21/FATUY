from pydantic import BaseModel


class AccountBalanceRequest(BaseModel):
    user_id: str