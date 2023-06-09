import logging
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

from src.api.v1.paginator import Paginator
from src.api.v1.schemas import UserReview, Review, ReviewSchema, Pagination
from src.db.mongo import get_mongo_db
from src.services.auth import User, JWTBearer
from src.services.user_activity import FilmService

router = APIRouter()

logger = logging.getLogger()


@router.post(
    '/',
    response_model=UserReview, description='Add review to the film',
    response_description='Added review to the film',
)
async def add_review(
    review: Review,
    user: User = Depends(JWTBearer()),
) -> UserReview:
    service = get_service()
    user_review = UserReview(user_id=user.id, **review.dict())
    return await service.add(user_review)


@router.delete(
    '/{review_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_review(review_id: str, user: User = Depends(JWTBearer())):
    service = get_service()
    await service.delete(review_id)
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content='OK')


@router.get(
    '/',
    response_model=ReviewSchema, description='Users reviews',
    response_description='Users reviews',
)
async def get_reviews(
    user: User = Depends(JWTBearer()),
    paginator: Paginator = Depends(),
) -> ReviewSchema:
    service = get_service()
    reviews = await service.get_by_user_id(
        str(user.id),
        page_number=paginator.page,
        per_page=paginator.per_page,
    )
    return ReviewSchema(
        meta=Pagination(
            page=paginator.page,
            per_page=paginator.per_page,
        ),
        data=reviews,
    )


@router.put(
    '/{review_id}',
    response_model=UserReview, description='Update review to the film',
    response_description='Update review to the film',
)
async def update_review(
    review_id: str,
    review: Review,
    user: User = Depends(JWTBearer()),
) -> UserReview:
    service = get_service()
    return await service.update(review_id, review)


@lru_cache()
def get_service():
    return FilmService(get_mongo_db(), 'reviews')
