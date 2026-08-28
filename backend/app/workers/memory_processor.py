import asyncio
import json
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from app.core.kafka import (
    KAFKA_BOOTSTRAP_SERVERS,
    CONVERSATION_EXPIRED_TOPIC,
    MEMORY_PROCESSING_GROUP,
)

from app.core.database import AsyncSessionLocal

from app.services.expired_conversation.expired_conversation_service import (
    expired_conversation_service,
)

from app.services.memory.memory_service import (
    memory_service,
)

from app.services.memory.memory_summary_service import (
    memory_summary_service,
)

from app.ai.providers import get_provider


async def process_message(event: dict):

    print("KAFKA EVENT RECEIVED:", event)

    expired_conversation_id = UUID(
        event["expired_conversation_id"]
    )

    async with AsyncSessionLocal() as db:

        expired_conversation = (
            await expired_conversation_service.get_by_id(
                db=db,
                expired_conversation_id=expired_conversation_id,
            )
        )

        if expired_conversation is None:

            print(
                "Expired conversation not found:",
                expired_conversation_id,
            )

            return


        if expired_conversation.status == "PROCESSED":

            print(
                "Conversation already processed:",
                expired_conversation_id,
            )

            return


        print(
            "PROCESSING CONVERSATION:",
            expired_conversation.id,
        )


        messages = expired_conversation.messages


        summary_messages = (
            memory_summary_service.build_messages(
                conversation_messages=messages,
            )
        )


        print("CALLING LLM FOR MEMORY SUMMARY")


        provider = get_provider(
            "ollama"
        )


        result = await provider.chat(
            messages=summary_messages,
        )


        memory_summary = result["content"]


        print(
            "LLM SUMMARY GENERATED:",
            memory_summary,
        )


        await memory_service.create_memory(
            db=db,
            user_id=expired_conversation.user_id,
            content=memory_summary,
            memory_type="conversation_summary",
            importance=1,
        )


        print("MEMORY SAVED")


        await expired_conversation_service.mark_processed(
            db=db,
            conversation=expired_conversation,
        )


        print(
            "CONVERSATION MARKED AS PROCESSED:",
            expired_conversation.id,
        )


async def consume():

    consumer = AIOKafkaConsumer(

        CONVERSATION_EXPIRED_TOPIC,

        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        group_id=MEMORY_PROCESSING_GROUP,

        enable_auto_commit=False,

        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),

    )


    print("STARTING KAFKA MEMORY WORKER")


    await consumer.start()


    try:

        print(
            "LISTENING TO TOPIC:",
            CONVERSATION_EXPIRED_TOPIC,
        )


        async for message in consumer:

            try:

                print(
                    "RAW KAFKA MESSAGE:",
                    message.value,
                )


                await process_message(
                    message.value
                )


                await consumer.commit()


                print("KAFKA OFFSET COMMITTED")


            except Exception as error:

                print(
                    "MEMORY PROCESSING FAILED:",
                    repr(error),
                )


                await asyncio.sleep(5)


    finally:

        await consumer.stop()


if __name__ == "__main__":

    asyncio.run(
        consume()
    )