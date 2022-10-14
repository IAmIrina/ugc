import logging
from datetime import datetime
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.api.v1.schemas import UGCEventPosted, UGCUserEvent
from src.core.config import settings
from src.db.kafka import get_kafka

module_logger = logging.getLogger('EventsService')


class EventsService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def post_event(self, event: UGCUserEvent) -> UGCEventPosted:
        topic = self._get_topic(event.type)
        key = self._get_key(event)

        posted_event = UGCEventPosted(**event.dict(), posted_at=datetime.utcnow())
        await self.kafka.send_and_wait(
            topic=topic,
            key=key.encode(),
            value=posted_event.json().encode(),
        )
        return posted_event

    @staticmethod
    def _get_key(event: UGCUserEvent) -> str:
        return f'{event.movie_id}+{str(event.user_id)}'

    def _get_topic(self, event_type: str) -> str:
        topic = event_type
        if topic not in self.kafka.client.cluster.topics():
            module_logger.error(
                f"Event topic doesn't exist in kafka, choosing default topic '{settings.ugc_default_topic}'",
            )
            topic = settings.ugc_default_topic
        return topic


@lru_cache()
def get_events_service(kafka: AIOKafkaProducer = Depends(get_kafka)) -> EventsService:
    return EventsService(kafka)
