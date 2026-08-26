from app.ai.providers import get_provider
from app.ai.schemas import AIRequestPlan


class AIPlanner:

    async def create_plan(
        self,
        user_id: str,
        message: str,
        provider_name: str,
    ) -> AIRequestPlan:

        provider = get_provider(
            provider_name
        )

        prompt = f"""
You are an AI query planner for a banking application.

Analyze the user's question and determine:

1. Which banking resource is required.
2. What filters are required.
3. Which fields are required in the response.

Available resources:

1. transactions
   Use for:
   - spending
   - payments
   - transaction history
   - merchants
   - credits
   - debits
   - transaction categories

2. account_balance
   Use for:
   - account balance
   - account information

3. loans
   Use for:
   - current loans
   - loan details
   - loan status

4. loan_history
   Use for:
   - loan payments
   - EMI history
   - loan repayment history

User question:
{message}

Return ONLY valid JSON.

The JSON must follow exactly this structure:

{{
    "resource": "transactions | loans | loan_history | account_balance",
    "filters": {{
        "field": "value"
    }},
    "required_fields": [
        "field1",
        "field2"
    ]
}}

Rules:

- Select only one resource.
- Include only filters relevant to the user's question.
- Include only fields needed to answer the user's question.
- Do not include explanations.
- Do not include markdown.
- Do not include any text outside the JSON.
"""

        response = await provider.generate(
            prompt=prompt
        )

        return AIRequestPlan.model_validate_json(
            response
        )


ai_planner = AIPlanner()