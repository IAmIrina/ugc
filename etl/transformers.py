from models import KafkaSchema


async def transform_kafka_record(record: dict) -> KafkaSchema:
    """Преобразует список записей из Kafka в валидированный список для ClickHouse"""
    for msg in record.values():
        struct = msg[0]
        schema = KafkaSchema(
            key=struct.key,
            movie_sec=struct.value['movie_sec'],
            movie_id=struct.value['movie_id'],
            user_id=struct.value['user_id'],
            posted_at=struct.value['posted_at'],
        )

    return schema

