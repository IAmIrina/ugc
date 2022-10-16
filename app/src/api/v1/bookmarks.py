import logging
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

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
    service = get_service()
    user_bookmark = Bookmark(user_id=user.id, **movie.dict())
    return await service.add(user_bookmark)


@router.get(
    '/',
    response_model=BookmarkSchema, description='Users bookmarks',
    response_description='Users bookmarks',
)
async def get_bookmarks(
    user: User = Depends(JWTBearer()),
    paginator: Paginator = Depends(),
) -> BookmarkSchema:
    service = get_service()
    bookmarks = await service.get_by_user_id(
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


@router.delete(
    '/{bookmark_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_bookmark(bookmark_id: str, user: User = Depends(JWTBearer())):
    service = get_service()
    await service.delete(bookmark_id)
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content='OK')


@lru_cache()
def get_service():
    return FilmService(get_mongo_db(), 'bookmarks')
