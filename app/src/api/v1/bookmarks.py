import logging

from fastapi import Depends, APIRouter

from src.api.v1.paginator import Paginator
from src.api.v1.schemas import Bookmark, Movie, BookmarkSchema, Pagination
from src.db.mongo import get_mongo_db
from src.services.auth import User, JWTBearer
from src.services.user_activity import FilmService

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
    service = FilmService(get_mongo_db(), 'bookmarks')
    user_bookmark = Bookmark(user_id=user.id, **movie.dict())
    return await service.add_data(user_bookmark)


@router.get(
    '/',
    response_model=BookmarkSchema, description='Users bookmarks',
    response_description='Users bookmarks',
)
async def get_bookmarks(
    user: User = Depends(JWTBearer()),
    paginator: Paginator = Depends(),
) -> BookmarkSchema:
    service = FilmService(get_mongo_db(), 'bookmarks')
    bookmarks = await service.get_data_by_user_id(
        str(user.id),
        page_number=paginator.page,
        per_page=paginator.per_page,
    )
    return BookmarkSchema(
        meta=Pagination(
            page=paginator.page,
            per_page=paginator.per_page,
        ),
        data=bookmarks,
    )
