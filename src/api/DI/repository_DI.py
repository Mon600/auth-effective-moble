from typing import Annotated

from fastapi import Depends

from src.api.DI.session_DI import SessionDep
from src.db.repositories.role_repository import RoleRepository
from src.db.repositories.user_repository import UserRepository


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

user_repository_DI = Annotated[UserRepository, Depends(get_user_repository)]



async def get_role_repository(session: SessionDep) -> RoleRepository:
    return  RoleRepository(session)

role_repository_DI = Annotated[RoleRepository, Depends(get_role_repository)]