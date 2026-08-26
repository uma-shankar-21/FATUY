from fastapi import FastAPI
from app.api.v1.router import api_router
from app.mcp.router import router as mcp_router
from app.ai.router import router as ai_router

app = FastAPI(
    title="Banking AI Assistant",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api/v1"
)
app.include_router(
    mcp_router,
)
app.include_router(ai_router)
@app.get("/")
async def root():
    return {
        "message": "Banking AI Assistant API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }