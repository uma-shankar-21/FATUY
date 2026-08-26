from fastapi import APIRouter

from app.mcp.schemas import MCPToolRequest
from app.mcp.server import execute_tool


router = APIRouter(
    prefix="/mcp",
    tags=["MCP"],
)


@router.post("/execute")
async def execute_mcp_tool(
    request: MCPToolRequest,
):

    return await execute_tool(request)