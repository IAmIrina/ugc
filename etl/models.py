from uuid import UUID
import datetime as dt

from pydantic import BaseModel


class MainConsumerModel(BaseModel):
    key: str
    posted_at: dt.datetime


class ConsumedMessage(MainConsumerModel):
    movie_sec: int
    movie_id: str
    user_id: UUID


class ClickhouseModel(BaseModel):
    event_time: str
    user_id: UUID
    movie_id: str
    viewed_frame: int


