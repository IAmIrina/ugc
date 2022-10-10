from models import ConsumedMessage


async def transform_kafka_record(batch: list) -> list[ConsumedMessage]:
    """Преобразует список сообщений из Kafka в валидированный список датаклассов."""
    validated_models = []
    for message in batch:
        validated_models.append(
            ConsumedMessage(
                key=message.key,
                movie_sec=message.value['movie_sec'],
                movie_id=message.value['movie_id'],
                user_id=message.value['user_id'],
                posted_at=message.value['posted_at'],
            ),
        )

    return validated_models
