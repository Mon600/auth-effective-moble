
from typing import List

from fastapi import HTTPException
from fastapi.params import Depends

from src.api.DI.user_DI import get_current_user_DI, get_current_user
from src.shared.enum_classes.roles import RoleEnum
from src.shared.pydantic_schemas.user import UserExtendedSchema


def require_role(roles: List[RoleEnum]):
    async def role_checker(user: get_current_user_DI):
        user_role = user.role_rel
        if not user_role or user_role.title not in roles:
            raise HTTPException(status_code=403, detail='No access')
        return user_role
    return role_checker



def require_rights(rights: List[str]):
    async def rights_checker(user: get_current_user_DI):
        user_role = user.role_rel
        for right in rights:
            if not getattr(user_role, right):
                raise HTTPException(status_code=403, detail='No access')
        return user_role
    return rights_checker