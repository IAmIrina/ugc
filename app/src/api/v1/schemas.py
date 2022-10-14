from datetime import datetime
from typing import Optional
from uuid import UUID

import orjson
from bson import ObjectId
from pydantic import BaseModel, Field


def orjson_dumps(decoded_data, *, default):
    return orjson.dumps(decoded_data, default=default).decode()


class BaseUGCModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UGCEvent(BaseUGCModel):
    type: str = Field(..., description='Type of event', example='views')
    movie_id: UUID = Field(..., description='Film id')
    movie_sec: int = Field(..., description='Number of seconds since the beginning of the movie')


class UGCUserEvent(UGCEvent):
    user_id: UUID = Field(..., description='Id of a user who generated the event')


class UGCEventPosted(UGCUserEvent):
    posted_at: Optional[datetime] = Field(None, description='When the event was posted')


class Movie(BaseUGCModel):
    movie_id: UUID = Field(..., description='Film id')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Grade(Movie):
    rating: int = Field(..., ge=0, le=10, description='Film rating')


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserGrade(Grade):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: UUID = Field(..., description='User id')

    class Config:
        # allow_population_by_field_name = True
        # arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "63493e4a57ce0a4356b3e37a",
                "movie_id": "92cb640a-79da-4aa5-b2aa-3ce2ad2dc920",
                "rating": 10,
                "user_id": "16168708-f1c0-4767-9b6d-8601d396fd91"
            }
        }


class Bookmark(Movie):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: UUID = Field(..., description='User id')

    class Config:
        # allow_population_by_field_name = True
        # arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "63493e4a57ce0a4356b3e37a",
                "movie_id": "92cb640a-79da-4aa5-b2aa-3ce2ad2dc920",
                "user_id": "16168708-f1c0-4767-9b6d-8601d396fd91"
            }
        }


class Review(Movie):
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserReview(Review):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: UUID = Field(..., description='User id')

    class Config:
        # allow_population_by_field_name = True
        # arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "63493e4a57ce0a4356b3e37a",
                "movie_id": "92cb640a-79da-4aa5-b2aa-3ce2ad2dc920",
                "user_id": "16168708-f1c0-4767-9b6d-8601d396fd91"
            }
        }