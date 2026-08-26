from typing import Any, Optional

from pydantic import BaseModel


class MCPToolResult(BaseModel):
    success: bool
    tool_name: str
    data: Optional[Any] = None
    error: Optional[str] = None


class MCPToolRequest(BaseModel):
    tool_name: str
    arguments: dict

MCP_TOOL_DEFINITIONS = [

    {
        "type": "function",
        "function": {
            "name": "get_transactions",
            "description": (
                "Get banking transactions for a user. "
                "Use filters to narrow the results. "
                "Request only the fields needed to answer the user's question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's UUID"
                    },
                    "transaction_type": {
                        "type": "string",
                        "enum": ["CREDIT", "DEBIT"]
                    },
                    "amount": {
                        "type": "number"
                    },
                    "description": {
                        "type": "string"
                    },
                    "merchant": {
                        "type": "string"
                    },
                    "category": {
                        "type": "string"
                    },
                    "status": {
                        "type": "string"
                    },
                    "transaction_date": {
                        "type": "string"
                    },
                    "start_date": {
                        "type": "string"
                    },
                    "end_date": {
                        "type": "string"
                    },

                    "response_fields": {
                        "type": "array",
                        "description": (
                            "Fields required in the response. "
                            "Only request fields needed to answer the user's question."
                        ),
                        "items": {
                            "type": "string",
                            "enum": [
                                "id",
                                "account_id",
                                "amount",
                                "transaction_type",
                                "description",
                                "merchant",
                                "category",
                                "status",
                                "currency",
                                "transaction_date",
                                "created_at"
                            ]
                        }
                    },

                    "aggregation": {
                        "type": "object",
                        "description": (
                            "Use aggregation when the user asks for a calculated "
                            "result such as total, count, average, minimum or maximum."
                        ),
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": [
                                    "sum",
                                    "count",
                                    "average",
                                    "min",
                                    "max"
                                ]
                            },
                            "field": {
                                "type": "string",
                                "enum": [
                                    "amount"
                                ]
                            }
                        },
                        "required": [
                            "operation"
                        ]
                    },

                    "limit": {
                        "type": "integer",
                        "description": (
                            "Maximum number of records to return."
                        )
                    }
                },
                "required": [
                    "user_id"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_loans",
            "description": (
                "Get all current loans belonging to a user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string"
                    }
                },
                "required": ["user_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_loan_history",
            "description": (
                "Get the loan payment history of a user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string"
                    }
                },
                "required": ["user_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": (
                "Get the current bank account balance "
                "and account information for a user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string"
                    }
                },
                "required": ["user_id"]
            }
        }
    }
]