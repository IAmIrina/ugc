from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase


class FilmService:
    def __init__(self, mongo_db: AsyncIOMotorDatabase, collection_name: str):
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    async def add_data(self, data):
        user_data = jsonable_encoder(data)
        if await self._find_data(user_data['movie_id'], user_data['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Already exists')
        new_data = await self.mongo_db[self.collection_name].insert_one(user_data)
        return await self.mongo_db[self.collection_name].find_one({'_id': new_data.inserted_id})

    async def _find_data(self, movie_id, user_id):
        return await self.mongo_db[self.collection_name].find_one(
            {'movie_id': movie_id, 'user_id': user_id},
        )
