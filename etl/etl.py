import aiokafka
import asyncio

from utils import bytes_to_dict_deserializer
from transformers import transform_kafka_record

async def main():
    consumer = aiokafka.AIOKafkaConsumer(
        "views",
        bootstrap_servers='0.0.0.0:9092',
        value_deserializer=bytes_to_dict_deserializer,
    )
    await consumer.start()
    try:
        while True:
            result = await consumer.getmany(timeout_ms=5 * 1000)
            if result:
                transformed = await transform_kafka_record(result)
                print(transformed)
    finally:
        # Не забываем останавливать Consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
