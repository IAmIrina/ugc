import asyncio
import logging

from transformers import transform_kafka_record
from consumers import get_kafka_consumer
from loaders import clickhouse_connect, load_data_to_clickhouse
from settings import etl_settings

logger = logging.getLogger()

async def etl_script():
    consumer = await get_kafka_consumer()
    clickhouse_client = clickhouse_connect()
    try:
        batch = []
        async for msg in consumer:
            batch.append(msg)
            if len(batch) == etl_settings.batch_size:
                await consumer.commit()
                # Трансформируем сообщения из Kafka
                transformed = await transform_kafka_record(batch)
                # Загружаем данные в Clickhouse
                load_data_to_clickhouse(transformed, clickhouse_client)
                batch = []
    finally:
        # Не забываем останавливать Consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(etl_script())
