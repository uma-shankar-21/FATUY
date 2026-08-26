from app.mcp.schemas import MCPToolRequest, MCPToolResult
from app.mcp.tools import MCP_TOOLS


async def execute_tool(
    request: MCPToolRequest,
):

    arguments = request.arguments.copy()

    response_fields = arguments.pop(
        "response_fields",
        None,
    )

    tool_handler = TOOL_REGISTRY.get(
        request.tool_name
    )

    if not tool_handler:

        raise ValueError(
            f"Unknown tool: {request.tool_name}"
        )

    result = await tool_handler(
        arguments
    )

    if not result.success:
        return result

    result.data = ResponseShaper.shape(
        data=result.data,
        fields=response_fields,
    )

    return result

    tool = MCP_TOOLS.get(request.tool_name)

    if not tool:
        return MCPToolResult(
            success=False,
            tool_name=request.tool_name,
            error=f"Unknown MCP tool: {request.tool_name}",
        )

    try:

        result = await tool(
            **request.arguments
        )

        return result

    except TypeError as error:

        return MCPToolResult(
            success=False,
            tool_name=request.tool_name,
            error=f"Invalid tool arguments: {str(error)}",
        )

    except Exception as error:

        return MCPToolResult(
            success=False,
            tool_name=request.tool_name,
            error=str(error),
        )