from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError


from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.db.base import get_db
users_route = APIRouter(prefix="/users")
from app.config import settings

async def get_users_id(
        token: Annotated[str,Depends(OAuth2PasswordBearer(tokenUrl="/users/token/"))],
) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user_id

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)