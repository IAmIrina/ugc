import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from utils import bytes_to_dict_deserializer
from settings import kafka_settings


logger = logging.getLogger()


async def get_kafka_consumer(topic: str = "views") -> AIOKafkaConsumer:
    """Подсоединяется к определенному топику и возвращает инстанc Consumer"""
    try:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=f'{kafka_settings.kafka_host}:{kafka_settings.kafka_port}',
            group_id="my_group",  # Consumer must be in a group to commit
            enable_auto_commit=False,  # Is True by default anyway
            auto_offset_reset="earliest",
            value_deserializer=bytes_to_dict_deserializer,
        )
        await consumer.start()
        return consumer
    except KafkaError as error:
        logger.error(f"Ошибка: Ошибка создания Kafka-Консьюмера ({error})")
