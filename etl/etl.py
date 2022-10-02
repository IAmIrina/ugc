import asyncio
import logging

from consumers import get_kafka_consumer
from loaders import clickhouse_connect, load_data_to_clickhouse
from settings import etl_settings
from transformers import transform_kafka_record

logger = logging.getLogger()


async def etl_script():
    consumer = await get_kafka_consumer()
    clickhouse_client = clickhouse_connect()
    try:
        batch = []
        async for msg in consumer:
            batch.append(msg)
            if len(batch) == etl_settings.batch_size:
                # Трансформируем сообщения из Kafka
                transformed = await transform_kafka_record(batch)
                # Загружаем данные в Clickhouse
                load_data_to_clickhouse(transformed, clickhouse_client)
                await consumer.commit()
                batch = []
    finally:
        # Не забываем останавливать Consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(etl_script())
