class BankingIntentService:

    def detect_intent(
        self,
        message: str,
    ) -> list[str]:

        message = message.lower()

        intents = []

        # Account / balance
        if any(
            keyword in message
            for keyword in [
                "balance",
                "account balance",
                "money in my account",
                "how much money",
                "bank account",
                "accounts",
            ]
        ):
            intents.append("accounts")

        # Transactions
        if any(
            keyword in message
            for keyword in [
                "transaction",
                "transactions",
                "spent",
                "spending",
                "payment",
                "purchase",
                "merchant",
                "expense",
                "expenses",
                "recent activity",
            ]
        ):
            intents.append("transactions")

        # Loans
        if any(
            keyword in message
            for keyword in [
                "loan",
                "emi",
                "outstanding",
                "interest",
                "due date",
                "monthly payment",
            ]
        ):
            intents.append("loans")

        return intents


banking_intent_service = BankingIntentService()