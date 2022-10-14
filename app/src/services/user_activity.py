from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.api.v1.schemas import UserGrade, Bookmark, UserReview


class FilmService:
    def __init__(self, mongo_db: AsyncIOMotorDatabase, collection_name: str):
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    async def add_data(self, data: UserGrade | Bookmark | UserReview) -> UserGrade | Bookmark | UserReview:
        user_data = jsonable_encoder(data)
        if await self._find_data(user_data['movie_id'], user_data['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Already exists')
        new_data = await self.mongo_db[self.collection_name].insert_one(user_data)
        created_data = await self.mongo_db[self.collection_name].find_one({"_id": new_data.inserted_id})
        return created_data

    async def _find_data(self, movie_id, user_id):
        data = await self.mongo_db[self.collection_name].find_one(
            {"movie_id": movie_id, "user_id": user_id}
        )
        return data
