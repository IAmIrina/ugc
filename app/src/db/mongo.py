from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

mongo: Optional[AsyncIOMotorClient] = None


def get_mongo_db() -> AsyncIOMotorDatabase:
    return mongo.films
