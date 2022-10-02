from datetime import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


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
    posted_at: datetime | None = Field(None, description='When the event was posted')
