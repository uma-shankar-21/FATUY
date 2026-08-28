import logging

import httpx

from app.core.config import settings


logger = logging.getLogger(__name__)


class EmbeddingService:

    async def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        logger.info(
            "Generating embedding | text_length=%s",
            len(text),
        )

        url = (
            f"{settings.OLLAMA_BASE_URL}"
            "/api/embeddings"
        )

        payload = {
            "model": "nomic-embed-text",
            "prompt": text,
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

        embedding = data["embedding"]

        logger.info(
            "Embedding generated | dimensions=%s",
            len(embedding),
        )

        return embedding


embedding_service = EmbeddingService()