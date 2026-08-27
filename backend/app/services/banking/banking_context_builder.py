import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.banking.banking_context_service import (
    banking_context_service,
)

from app.services.banking.intent_service import (
    banking_intent_service,
)


class BankingContextBuilder:

    async def build_context(
        self,
        db: AsyncSession,
        user_id,
        message: str,
    ) -> dict:

        intents = banking_intent_service.detect_intent(
            message
        )

        context = {
            "intents": intents,
            "accounts": [],
            "transactions": [],
            "loans": [],
            "loan_payments": [],
        }

        if "accounts" in intents:

            context["accounts"] = (
                await banking_context_service.get_accounts(
                    db=db,
                    user_id=user_id,
                )
            )

        if "transactions" in intents:

            context["transactions"] = (
                await banking_context_service.get_recent_transactions(
                    db=db,
                    user_id=user_id,
                )
            )

        if "loans" in intents:

            context["loans"] = (
                await banking_context_service.get_loans(
                    db=db,
                    user_id=user_id,
                )
            )

            context["loan_payments"] = (
                await banking_context_service.get_recent_loan_payments(
                    db=db,
                    user_id=user_id,
                )
            )

        return context

    def format_context(
        self,
        context: dict,
    ) -> str:

        return json.dumps(
            context,
            indent=2,
            default=str,
        )


banking_context_builder = BankingContextBuilder()