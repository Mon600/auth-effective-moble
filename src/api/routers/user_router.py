from asyncpg import PostgresError


from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import Response

from src.api.DI.service_DI import user_service_DI
from src.api.DI.user_DI import get_current_user_DI
from src.shared.pydantic_schemas.user import UserBase


router = APIRouter(prefix='/user')


@router.get('/')
async def get_user_data(user_id: get_current_user_DI, service: user_service_DI) -> UserBase:
    try:

        user_data = await service.get_user_by_id(user_id)
        return user_data
    except ValueError:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    except PostgresError:
        raise HTTPException(status_code=500, detail="Ошибка сервера, повторите попытку позже")


@router.put('/')
async def update_data(user_id: get_current_user_DI, data: UserBase, service: user_service_DI) -> UserBase:
    try:
        new_data = await service.update(user_id, data)
        return new_data
    except ValueError:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    except PostgresError:
        raise HTTPException(status_code=500, detail="Ошибка сервера, повторите попытку позже")


@router.delete('/')
async def delete_account(response: Response, user_id: get_current_user_DI, service: user_service_DI) -> UserBase:
    try:
        deleted_account_data = await service.deactivate_account(user_id)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return deleted_account_data
    except ValueError:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')
    except PostgresError:
        raise HTTPException(status_code=500, detail="Ошибка сервера, повторите попытку позже")