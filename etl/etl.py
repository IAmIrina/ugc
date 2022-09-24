import aiokafka
import asyncio


async def main():
    consumer = aiokafka.AIOKafkaConsumer(
        "views",
        bootstrap_servers='0.0.0.0:9092',
        max_poll_records=2
    )
    await consumer.start()

    await consumer.getmany()

    try:
        async for msg in consumer:
            print(msg)
    finally:
        # Не забываем останавливать Consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
