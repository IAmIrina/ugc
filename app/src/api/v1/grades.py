import logging
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

from src.api.v1.paginator import Paginator
from src.api.v1.schemas import UserGrade, Grade, GradeSchema, Pagination
from src.db.mongo import get_mongo_db
from src.services.auth import User, JWTBearer
from src.services.user_activity import FilmService

router = APIRouter()

logger = logging.getLogger()


@router.post(
    '/',
    response_model=UserGrade, description='Add grade to the film',
    response_description='Added grade to the film',
)
async def add_grade(
    grade: Grade,
    user: User = Depends(JWTBearer()),
) -> UserGrade:
    service = get_service()
    user_grade = UserGrade(user_id=user.id, **grade.dict())
    return await service.add(user_grade)


@router.delete(
    '/{grade_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_review(grade_id: str, user: User = Depends(JWTBearer())):
    service = get_service()
    await service.delete(grade_id)
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content='OK')


@router.get(
    '/',
    response_model=GradeSchema, description='Users grades',
    response_description='Users grades',
)
async def get_reviews(
    user: User = Depends(JWTBearer()),
    paginator: Paginator = Depends(),
) -> GradeSchema:
    service = get_service()
    grades = await service.get_by_user_id(
        str(user.id),
        page_number=paginator.page,
        per_page=paginator.per_page,
    )
    return GradeSchema(
        meta=Pagination(
            page=paginator.page,
            per_page=paginator.per_page,
        ),
        data=grades,
    )


@router.put(
    '/{grade_id}',
    response_model=UserGrade, description='Add grade to the film',
    response_description='Added grade to the film',
)
async def update_grade(
    grade_id: str,
    grade: Grade,
    user: User = Depends(JWTBearer()),
) -> UserGrade:
    service = get_service()
    # user_grade = UserGrade(user_id=user.id, **grade.dict())
    return await service.update(grade_id, grade)


@lru_cache()
def get_service():
    return FilmService(get_mongo_db(), 'grades')
