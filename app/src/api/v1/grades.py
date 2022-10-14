import logging

from fastapi import Depends, APIRouter

from src.api.v1.schemas import UserGrade, Grade
from src.db.mongo import get_mongo_db
from src.services.auth import User, JWTBearer
from src.services.events import FilmService

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
    # created_grade = await service.add_grade(user_grade)
    created_grade = await service.add_data(user_grade)
    return created_grade
