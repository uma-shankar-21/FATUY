import json
import logging

from aiokafka import AIOKafkaProducer

from app.core.kafka import (
    KAFKA_BOOTSTRAP_SERVERS,
)


logger = logging.getLogger(__name__)


class KafkaProducerService:

    def __init__(self):

        self.producer: AIOKafkaProducer | None = None


    async def start(self):

        if self.producer is not None:

            logger.info(
                "Kafka producer already started"
            )

            return

        logger.info(
            "Starting Kafka producer | kafka=%s",
            KAFKA_BOOTSTRAP_SERVERS,
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda value: json.dumps(
                value
            ).encode("utf-8"),
        )

        await self.producer.start()

        logger.info(
            "Kafka producer connected successfully"
        )


    async def stop(self):

        if self.producer is None:
            return

        logger.info(
            "Stopping Kafka producer"
        )

        await self.producer.stop()

        self.producer = None


    async def send(
        self,
        topic: str,
        message: dict,
    ):

        if self.producer is None:

            logger.warning(
                "Kafka producer was not started. Starting now."
            )

            await self.start()

        logger.info(
            "Sending Kafka message | "
            "topic=%s | message=%s",
            topic,
            message,
        )

        metadata = await self.producer.send_and_wait(
            topic,
            message,
        )

        logger.info(
            "Kafka message sent successfully | "
            "topic=%s | partition=%s | offset=%s",
            metadata.topic,
            metadata.partition,
            metadata.offset,
        )


kafka_producer = KafkaProducerService()