import logging
from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.v1.schemas import UGCEventPosted, UGCUserEvent, UserGrade, Bookmark, UserReview
from src.core.config import settings
from src.db.kafka import get_kafka
from src.db.mongo import get_mongo_db

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


class FilmService:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db

    async def add_grade(self, user_grade: UserGrade) -> UserGrade:
        user_grade = jsonable_encoder(user_grade)
        if await self.find_grade(user_grade['movie_id'], user_grade['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='This grade already exists')
        new_grade = await self.mongo_db["grades"].insert_one(user_grade)
        created_grade = await self.mongo_db["grades"].find_one({"_id": new_grade.inserted_id})
        return created_grade

    async def add_bookmark(self, user_bookmark: Bookmark) -> Bookmark:
        user_bookmark = jsonable_encoder(user_bookmark)
        if await self.find_bookmark(user_bookmark['movie_id'], user_bookmark['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='This bookmark already exists')
        new_bookmark = await self.mongo_db["bookmarks"].insert_one(user_bookmark)
        created_bookmark = await self.mongo_db["bookmarks"].find_one({"_id": new_bookmark.inserted_id})
        return created_bookmark

    async def add_review(self, user_review: UserReview) -> UserReview:
        user_review = jsonable_encoder(user_review)
        if await self.find_review(user_review['movie_id'], user_review['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='This review already exists')
        new_review = await self.mongo_db["reviews"].insert_one(user_review)
        created_review = await self.mongo_db["reviews"].find_one({"_id": new_review.inserted_id})
        return created_review

    async def find_grade(self, movie_id, user_id):
        grade = await self.mongo_db["grades"].find_one(
            {"movie_id": movie_id, "user_id": user_id}
        )
        return grade

    async def find_bookmark(self, movie_id, user_id):
        bookmark = await self.mongo_db["bookmarks"].find_one(
            {"movie_id": movie_id, "user_id": user_id}
        )
        return bookmark

    async def find_review(self, movie_id, user_id):
        review = await self.mongo_db["reviews"].find_one(
            {"movie_id": movie_id, "user_id": user_id}
        )
        return review


@lru_cache()
def get_events_service(kafka: AIOKafkaProducer = Depends(get_kafka)) -> EventsService:
    return EventsService(kafka)


@lru_cache()
def get_mongo_db_service(mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> FilmService:
    return FilmService(mongo_db)
