import aiokafka
import asyncio

from utils import bytes_to_dict_deserializer
from transformers import transform_kafka_record
from consumers import get_consumer

async def etl_script():
    consumer = await get_consumer()
    try:
        batch = []
        async for msg in consumer:
            batch.append(msg)
            if len(batch) == 3:
                await consumer.commit()
                transformed = await transform_kafka_record(batch)
                print(transformed)

                batch = []
    finally:
        # Не забываем останавливать Consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(etl_script())
