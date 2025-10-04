from typing import Annotated

from fastapi import Depends

from src.api.DI.repository_DI import user_repository_DI, role_repository_DI
from src.services.auth_service import AuthService
from src.services.role_service import RoleService
from src.services.user_service import UserService


async def get_user_service(repository: user_repository_DI) -> UserService:
    return UserService(repository)

user_service_DI = Annotated[UserService, Depends(get_user_service)]


async def get_role_service(repository: role_repository_DI) -> RoleService:
    return RoleService(repository)


role_service_DI = Annotated[RoleService, Depends(get_role_service)]


async def get_auth_service(repository: user_repository_DI, role_service: role_service_DI) -> AuthService:
    return AuthService(repository, role_service)

auth_service_DI = Annotated[AuthService, Depends(get_auth_service)]