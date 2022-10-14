import logging

from fastapi import Depends, APIRouter

from src.api.v1.schemas import UserReview, Review
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
    service = FilmService(get_mongo_db(), 'reviews')
    user_review = UserReview(user_id=user.id, **review.dict())
    return await service.add_data(user_review)
