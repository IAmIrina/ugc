import logging

from fastapi import APIRouter, Depends

from src.api.v1.schemas import UGCEventPosted, UGCEvent, UGCUserEvent, Grade, UserGrade, Bookmark, Movie, UserReview, \
    Review
from src.db.mongo import get_mongo_db
from src.services.auth import JWTBearer, User
from src.services.events import get_events_service, EventsService, FilmService

router = APIRouter()

logger = logging.getLogger()


@router.post(
    '/',
    response_model=UGCEventPosted, description='Posting UGC events',
    response_description='Posted UGC event with timestamp',
)
async def post_event(
        event: UGCEvent,
        service: EventsService = Depends(get_events_service),
        user: User = Depends(JWTBearer()),
) -> UGCEventPosted:
    logger.warning('event received')
    user_event = UGCUserEvent(user_id=user.id, **event.dict())
    return await service.post_event(user_event)


@router.post(
    '/grade',
    response_model=UserGrade, description='Add grade to the film',
    response_description='Added grade to the film',
)
async def add_grade(
        grade: Grade,
        user: User = Depends(JWTBearer()),
) -> UserGrade:
    service = FilmService(get_mongo_db())
    user_grade = UserGrade(user_id=user.id, **grade.dict())
    created_grade = await service.add_grade(user_grade)
    return created_grade


@router.post(
    '/bookmark',
    response_model=Bookmark, description='Add bookmark to the film',
    response_description='Added bookmark to the film',
)
async def add_grade(
        movie: Movie,
        user: User = Depends(JWTBearer()),
) -> Bookmark:
    service = FilmService(get_mongo_db())
    user_bookmark = Bookmark(user_id=user.id, **movie.dict())
    created_bookmark = await service.add_bookmark(user_bookmark)
    return created_bookmark


@router.post(
    '/review',
    response_model=UserReview, description='Add review to the film',
    response_description='Added review to the film',
)
async def add_review(
        review: Review,
        user: User = Depends(JWTBearer()),
) -> UserReview:
    service = FilmService(get_mongo_db())
    user_review = UserReview(user_id=user.id, **review.dict())
    created_review = await service.add_review(user_review)
    return created_review
