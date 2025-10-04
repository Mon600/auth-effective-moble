from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from src.api.DI.RBAC_DI import require_role, require_rights
from src.api.DI.service_DI import user_service_DI, role_service_DI
from src.shared.enum_classes.roles import RoleEnum
from src.shared.pydantic_schemas.role import RoleSchema, Rights
from src.shared.pydantic_schemas.user import UserBase

router = APIRouter(prefix='/protect')


@router.get('/users')
async def get_all_users(service: user_service_DI,
                        role = Depends(require_role([RoleEnum.admin, RoleEnum.superuser]))
                        ) -> List[UserBase]:
    """Эндопинт для модераторов/админов"""
    users =  await service.get_all_users()
    return users


@router.put('/roles/{role_id}')
async def change_roles(role_id: int,
                       service: role_service_DI,
                       new_rights: Rights,
                       role = Depends(require_role([RoleEnum.admin]))
                       ) -> RoleSchema:
    """Эндпоинт для смены прав у ролей(только для админов)"""
    new_role = await service.update_role(role_id, new_rights)
    return new_role


@router.put('/user/{user_id}/role/{role_id}')
async def change_user_role(user_id: int,
                           role_id: int,
                           service: user_service_DI,
                           role = Depends(require_role([RoleEnum.admin]))
                           ) -> UserBase:
    """Изменение роли пользователя"""
    new_user_data = await service.change_user_role(user_id, role_id)
    return new_user_data

@router.put('/set-status')
async def change_user_status(user_id: int,
                             status: bool,
                             service: user_service_DI,
                             role = Depends(require_role([RoleEnum.admin]))) -> UserBase:
    """Эндпоинт смены статуса is_active пользоватлея по id (Только для админов)"""
    changed_account = await service.deactivate_account(user_id, status)
    return changed_account



@router.get('/')
async def get_secret_info(rights = Depends(require_rights(['access_to_protected_resources']))):
    """Эндпоинт для проверки работы прав доступа"""
    return {"ok": True, 'detail': "Some secret info"}

