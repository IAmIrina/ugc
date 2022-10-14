import logging

from fastapi import Depends, APIRouter

from src.api.v1.schemas import Bookmark, Movie
from src.db.mongo import get_mongo_db
from src.services.auth import User, JWTBearer
from src.services.events import FilmService

router = APIRouter()

logger = logging.getLogger()


@router.post(
    '/',
    response_model=Bookmark, description='Add bookmark to the film',
    response_description='Added bookmark to the film',
)
async def add_bookmark(
        movie: Movie,
        user: User = Depends(JWTBearer()),
) -> Bookmark:
    service = FilmService(get_mongo_db())
    user_bookmark = Bookmark(user_id=user.id, **movie.dict())
    created_bookmark = await service.add_bookmark(user_bookmark)
    return created_bookmark
