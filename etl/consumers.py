import logging
import time

from aiokafka import AIOKafkaConsumer

from settings import kafka_settings
from utils import bytes_to_dict_deserializer, backoff

logger = logging.getLogger()


@backoff()
async def get_kafka_consumer(topic: str = 'views') -> AIOKafkaConsumer:
    """Подсоединяется к определенному топику и возвращает инстанc Consumer."""
    time.sleep(10)
    try:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=f'{kafka_settings.kafka_host}:{kafka_settings.kafka_port}',
            group_id='my_group',  # Consumer must be in a group to commit
            enable_auto_commit=False,  # Is True by default anyway
            auto_offset_reset='earliest',
            value_deserializer=bytes_to_dict_deserializer,
        )
        await consumer.start()
        logger.warning('Consumer Created')
        return consumer
    except Exception:
        logger.warning('Consumer Creation Error')
