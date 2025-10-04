from typing import Dict, Any

import sqlalchemy.exc
from asyncpg import PostgresError
from fastapi import APIRouter, HTTPException

from starlette.responses import Response

from src.api.DI.service_DI import auth_service_DI
from src.api.DI.user_DI import get_refresh_token_DI
from src.shared.pydantic_schemas.user import UserLogin, UserBase, UserCreate

router = APIRouter()


@router.post('/register', status_code=201)
async def register_user(response: Response, data: UserCreate, service: auth_service_DI) -> Dict[str, Any]:
    try:
        register_data = await service.register(data)
        response.set_cookie('access_token',
                            register_data.access_token,
                            expires=900,
                            httponly=True,
                            samesite='lax',
                            secure=True
                            )
        response.set_cookie('refresh_token',
                            register_data.refresh_token,
                            expires=43200,
                            httponly=True,
                            samesite='lax',
                            secure=True
                            )
        return {'ok': True, 'detail': f"Account successfully created. Your ID: {register_data.user_id}"}
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409, detail='Пользователь с таким email уже существует.')
    except PostgresError:
        raise HTTPException(status_code=500, detail="Ошибка сервера, повторите попытку позже")


@router.post('/login')
async def login(response: Response, data: UserLogin, service: auth_service_DI) -> UserBase:
    try:
        login_data = await service.login(data)
        response.set_cookie('access_token',
                            login_data.access_token,
                            expires=900,
                            httponly=True,
                            samesite='lax',
                            secure=True
                            )
        response.set_cookie('refresh_token',
                            login_data.refresh_token,
                            expires=43200,
                            httponly=True,
                            samesite='lax',
                            secure=True
                            )
        return login_data.user
    except ValueError:
        raise HTTPException(status_code=403, detail="Неверный email или пароль")
    except PostgresError:
        raise HTTPException(status_code=500, detail="Ошибка сервера, повторите попытку позже")


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'ok': True, 'detail': 'Вы успешно вышли из системы.'}


@router.post('/refresh')
async def refresh(response:Response, refresh_token: get_refresh_token_DI, service: auth_service_DI):
    try:
        access_token = await service.refresh(refresh_token)
        response.set_cookie('access_token',
                            access_token,
                            expires=900,
                            httponly=True,
                            samesite='lax',
                            secure=True
                            )
        return access_token
    except ValueError:
        raise HTTPException(401, detail='Invalid token')