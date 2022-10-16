from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase


class FilmService:
    def __init__(self, mongo_db: AsyncIOMotorDatabase, collection_name: str):
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    async def add(self, data):
        user_data = jsonable_encoder(data)
        if await self._find(user_data['movie_id'], user_data['user_id']):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Already exists')
        new_data = await self.mongo_db[self.collection_name].insert_one(user_data)  # noqa: WPS204
        return await self.mongo_db[self.collection_name].find_one({'_id': new_data.inserted_id})

    async def delete(self, _id):
        delete_result = await self.mongo_db[self.collection_name].delete_one({'_id': _id})

        if delete_result.deleted_count != 1:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')

    async def get_by_user_id(self, user_id, page_number: int = 1, per_page: int = 50):
        return await (self.mongo_db[self.collection_name]  # noqa: WPS221
                      .find({'user_id': user_id})  # noqa: WPS318
                      .sort('_id')
                      .skip((page_number - 1) * per_page)
                      .limit(per_page)
                      .to_list(per_page)  # noqa: C812
                      )

    async def update(self, _id, data):
        user_data = jsonable_encoder(data)
        data = {key: value for key, value in user_data.items() if value is not None}  # noqa: WPS221

        if len(data) >= 1:  # noqa: WPS507
            update_result = await self.mongo_db[self.collection_name].update_one(
                {'_id': _id}, {'$set': data},
            )  # noqa: WPS221

            if update_result.modified_count == 1:
                return await self.mongo_db[self.collection_name].find_one({'_id': _id})

        if existing_data := await self.mongo_db[self.collection_name].find_one({'_id': _id}):  # noqa: WPS332
            return existing_data

        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')

    async def _find(self, movie_id, user_id):
        return await self.mongo_db[self.collection_name].find_one(
            {'movie_id': movie_id, 'user_id': user_id},
        )
