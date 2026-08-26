import json
import logging

from app.core.config import settings
from app.ai.providers import get_provider
from app.mcp.schemas import MCPToolRequest
from app.mcp.server import execute_tool
from app.mcp.schemas import MCP_TOOL_DEFINITIONS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


class AIService:

    async def chat(
        self,
        user_id: str,
        message: str,
    ) -> dict:

        logger.info("========================================")
        logger.info("AI CHAT REQUEST STARTED")
        logger.info("User ID: %s", user_id)
        logger.info("User message: %s", message)
        logger.info("========================================")

        messages = [
            {
                "role": "system",
                "content": (
                    """You are an intelligent banking assistant.

                    Your job is to help users answer questions about their banking data.

                    When the information required to answer a question is not already
                    available in the conversation, use the available tools to retrieve it.

                    After receiving tool results:

                    - Treat the returned data as factual source data.
                    - Continue solving the user's original request.
                    - Infer the required operation from the user's question.
                    - Perform any necessary reasoning, filtering, aggregation,
                    comparison, summarization, or calculation.
                    - Return the answer directly to the user.

                    Do not switch into explaining the tool response or its JSON structure
                    unless the user explicitly asks for that.

                    Do not invent banking information. If the available data is insufficient,
                    clearly explain what information is missing."""
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        logger.info(
            "Initial messages created: %s",
            json.dumps(messages, indent=2, default=str),
        )

        logger.info(
            "Available MCP tools: %s",
            json.dumps(
                MCP_TOOL_DEFINITIONS,
                indent=2,
                default=str,
            ),
        )

        providers = [
            provider.strip()
            for provider in
            settings.AI_PROVIDER_PRIORITY.split(",")
        ]

        logger.info(
            "AI provider priority: %s",
            providers,
        )

        for provider_name in providers:

            try:

                logger.info("----------------------------------------")
                logger.info(
                    "Trying AI provider: %s",
                    provider_name,
                )
                logger.info("----------------------------------------")

                provider = get_provider(provider_name)

                logger.info(
                    "Provider instance created: %s",
                    provider,
                )

                result = await self._process_with_provider(
                    provider=provider,
                    user_id=user_id,
                    messages=messages,
                )

                logger.info(
                    "Final AI response from provider %s: %s",
                    provider_name,
                    result,
                )

                logger.info("AI CHAT REQUEST COMPLETED")
                logger.info("========================================")

                return {
                    "success": True,
                    "provider": provider_name,
                    "response": result,
                }

            except Exception as error:

                logger.exception(
                    "Provider failed: %s - %s",
                    provider_name,
                    error,
                )

                continue

        logger.error(
            "All AI providers failed",
        )

        return {
            "success": False,
            "provider": None,
            "response": (
                "😕 Our AI assistant is currently unavailable. "
                "Please try again in a little while."
            ),
        }

    async def _process_with_provider(
        self,
        provider,
        user_id: str,
        messages: list[dict],
    ) -> str:

        max_rounds = settings.AI_MAX_TOOL_ROUNDS

        logger.info(
            "Maximum tool rounds: %s",
            max_rounds,
        )

        for round_number in range(max_rounds):

            logger.info("========================================")
            logger.info(
                "STARTING AI ROUND %s",
                round_number + 1,
            )
            logger.info("========================================")

            logger.info(
                "Messages being sent to AI provider:"
            )

            logger.info(
                json.dumps(
                    messages,
                    indent=2,
                    default=str,
                )
            )

            logger.info(
                "Calling provider.chat()"
            )

            result = await provider.chat(
                messages=messages,
                tools=MCP_TOOL_DEFINITIONS,
            )

            logger.info(
                "RAW PROVIDER RESPONSE:"
            )

            logger.info(
                json.dumps(
                    result,
                    indent=2,
                    default=str,
                )
            )

            tool_calls = result.get(
                "tool_calls",
                [],
            )

            logger.info(
                "Tool calls found: %s",
                tool_calls,
            )

            if not tool_calls:

                final_content = (
                    result.get("content")
                    or
                    "I'm sorry, I couldn't generate a response."
                )

                logger.info(
                    "No tool calls requested."
                )

                logger.info(
                    "Final content: %s",
                    final_content,
                )

                return final_content

            logger.info(
                "Number of tool calls: %s",
                len(tool_calls),
            )

            for tool_call in tool_calls:

                logger.info("----------------------------------------")
                logger.info(
                    "PROCESSING TOOL CALL"
                )
                logger.info("----------------------------------------")

                logger.info(
                    "Tool call received: %s",
                    json.dumps(
                        tool_call,
                        indent=2,
                        default=str,
                    ),
                )

                arguments = tool_call["arguments"]

                logger.info(
                    "Raw tool arguments: %s",
                    arguments,
                )

                if isinstance(arguments, str):

                    logger.info(
                        "Tool arguments are string. "
                        "Converting JSON string to dictionary."
                    )

                    arguments = json.loads(
                        arguments
                    )

                logger.info(
                    "Parsed tool arguments: %s",
                    json.dumps(
                        arguments,
                        indent=2,
                        default=str,
                    ),
                )

                # Remove None values
                arguments = {
                    key: value
                    for key, value in arguments.items()
                    if value is not None
                }


                # Remove fake/default amount
                if arguments.get("amount") == 0:
                    arguments.pop("amount")


                # Normalize category
                if arguments.get("category"):
                    arguments["category"] = arguments["category"].upper()

                arguments["user_id"] = user_id

                logger.info(
                    "Final tool arguments after injecting user_id: %s",
                    json.dumps(
                        arguments,
                        indent=2,
                        default=str,
                    ),
                )

                logger.info(
                    "Executing MCP tool: %s",
                    tool_call["name"],
                )

                tool_result = await execute_tool(
                    MCPToolRequest(
                        tool_name=tool_call["name"],
                        arguments=arguments,
                    )
                )

                logger.info(
                    "MCP TOOL RESULT:"
                )

                logger.info(
                    tool_result.model_dump_json(
                        indent=2,
                    )
                )

                logger.info(
                    "Adding assistant message "
                    "to conversation"
                )

                messages.append({
                    "role": "assistant",
                    "content": result.get("content"),
                })

                logger.info(
                    "Adding tool result "
                    "to conversation"
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id"),
                    "content": (
                        tool_result
                        .model_dump_json()
                    ),
                })

                logger.info(
                    "Updated messages after tool execution:"
                )

                logger.info(
                    json.dumps(
                        messages,
                        indent=2,
                        default=str,
                    )
                )

        logger.warning(
            "Maximum tool rounds reached"
        )

        return (
            "I couldn't complete the requested banking "
            "information lookup. Please try again."
        )


ai_service = AIService()