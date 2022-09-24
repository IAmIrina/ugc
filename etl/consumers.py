import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from utils import bytes_to_dict_deserializer


logger = logging.getLogger()


async def get_consumer(topic: str = "views") -> AIOKafkaConsumer:
    """Подсоединяется к определенному топику и возвращает инстанc Consumer"""
    try:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers='0.0.0.0:9092',
            group_id="my_group",  # Consumer must be in a group to commit
            enable_auto_commit=False,  # Is True by default anyway
            auto_offset_reset="earliest",
            value_deserializer=bytes_to_dict_deserializer,
        )
        await consumer.start()
        return consumer
    except KafkaError as error:
        logger.error(f"Ошибка: Ошибка создания консьюмера ({error})")
