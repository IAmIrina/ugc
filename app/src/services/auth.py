import logging
import time
from http import HTTPStatus
from uuid import UUID

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from src.core.config import api_settings

logger = logging.getLogger()


class User(BaseModel):
    id: UUID
    roles: list[str]


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            return

        if not credentials.scheme == 'Bearer':
            logger.warning(credentials.scheme)
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Invalid authentication scheme.')
        payload = self.verify_jwt(credentials.credentials)
        if not payload:
            logger.warning("PAYLOAD NO")
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Invalid token or expired token.')
        return User(id=payload['sub'], roles=payload['roles'])

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            payload = decodeJWT(jwtoken)
        except jwt.exceptions.PyJWTError:
            payload = None

        return payload


def decodeJWT(token: str) -> dict:
    logger.warning(token)
    try:
        decoded_token = jwt.decode(token, api_settings.jwt_secret, algorithms=[api_settings.jwt_algorithm])
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except jwt.exceptions.PyJWTError:
        return {}
