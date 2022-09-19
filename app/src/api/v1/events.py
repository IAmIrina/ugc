from fastapi import APIRouter, Depends

from app.src.api.v1.schemas import UGCEventPosted, UGCEvent, UGCUserEvent
from app.src.services.auth import JWTBearer, User
from app.src.services.events import get_events_service, EventsService

router = APIRouter()


@router.post(
    '/',
    response_model=UGCEventPosted, description='Posting UGC events',
    response_description='Posted UGC event with timestamp'
)
async def post_event(
        event: UGCEvent,
        service: EventsService = Depends(get_events_service),
        user: User = Depends(JWTBearer())
) -> UGCEventPosted:
    user_event = UGCUserEvent(user_id=user.id, **event.dict())
    posted_event = await service.post_event(user_event)
    return posted_event
