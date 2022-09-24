from uuid import UUID
import datetime as dt

from pydantic import BaseModel


class MainKafkaModel(BaseModel):
    key: str
    posted_at: dt.datetime


class KafkaSchema(MainKafkaModel):
    movie_sec: int
    movie_id: str
    user_id: UUID
