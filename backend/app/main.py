from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Banking AI Assistant",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api/v1"
)

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