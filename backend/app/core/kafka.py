from app.core.config import settings

KAFKA_BOOTSTRAP_SERVERS = (
    settings.KAFKA_BOOTSTRAP_SERVERS
)

CONVERSATION_EXPIRED_TOPIC = (
    "conversation-expired"
)

MEMORY_PROCESSING_GROUP = (
    "memory-processing-group"
)
