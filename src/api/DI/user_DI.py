from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from jose import JWTError
from starlette.requests import Request

from src.api.DI.service_DI import user_service_DI
from src.shared.pydantic_schemas.user import UserExtendedSchema

from src.shared.security.jwt import decode_token


async def get_current_user(request: Request, service: user_service_DI) -> UserExtendedSchema:
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        payload = await decode_token(access_token)
        user_id = payload.get('user_id', None)
        user_data = await service.get_user_with_role(user_id)
        return user_data
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')


get_current_user_DI = Annotated[UserExtendedSchema, Depends(get_current_user)]


async def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    return token


get_refresh_token_DI = Annotated[str, Depends(get_refresh_token)]


