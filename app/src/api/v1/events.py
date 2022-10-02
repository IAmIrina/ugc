from fastapi import APIRouter, Depends

from src.api.v1.schemas import UGCEventPosted, UGCEvent, UGCUserEvent
from src.services.auth import JWTBearer, User
from src.services.events import get_events_service, EventsService

import logging

router = APIRouter()

logger = logging.getLogger()

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
    logger.warning('event received')
    user_event = UGCUserEvent(user_id=user.id, **event.dict())
    posted_event = await service.post_event(user_event)
    return posted_event
