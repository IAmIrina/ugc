import logging
from http import HTTPStatus

from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

from src.api.v1.schemas import UserGrade, Grade
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
    service = FilmService(get_mongo_db(), 'grades')
    user_grade = UserGrade(user_id=user.id, **grade.dict())
    return await service.add(user_grade)


@router.delete(
    '/{grade_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_review(grade_id: str, user: User = Depends(JWTBearer())):
    service = FilmService(get_mongo_db(), 'grades')
    await service.delete(grade_id)
    return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content='OK')
