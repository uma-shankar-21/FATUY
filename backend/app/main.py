import asyncio
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.ai.router import router
from app.services.memory.router import (
    router as memory_router,
)

from app.services.kafka.kafka_producer import (
    kafka_producer,
)

from app.workers.outbox_publisher import (
    outbox_publisher,
)

from app.workers.session_expiration_worker import (
    session_expiration_worker,
)

from app.api.routes.customer import router as customer_router

from app.api.routes.auth import (
    router as auth_router,
)

from app.api.routes.dashboard import (
    router as dashboard_router,
)

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # ==========================================
    # START KAFKA PRODUCER
    # ==========================================

    await kafka_producer.start()


    # ==========================================
    # START BACKGROUND WORKERS
    # ==========================================

    outbox_task = asyncio.create_task(
        outbox_publisher.run()
    )

    session_expiration_task = asyncio.create_task(
        session_expiration_worker.run()
    )


    try:

        yield

    finally:

        # ==========================================
        # STOP BACKGROUND WORKERS
        # ==========================================

        outbox_task.cancel()

        session_expiration_task.cancel()


        # Wait for workers to shut down cleanly
        await asyncio.gather(
            outbox_task,
            session_expiration_task,
            return_exceptions=True,
        )


        # ==========================================
        # STOP KAFKA PRODUCER
        # ==========================================

        await kafka_producer.stop()


app = FastAPI(
    title="Banking AI Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# API ROUTERS
# ==========================================

app.include_router(
    api_router,
    prefix="/api/v1",
)

app.include_router(
    router,
)

app.include_router(
    memory_router,
)

app.include_router(customer_router)

app.include_router(
    auth_router
)

app.include_router(
    dashboard_router
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