from typing import List

from src.db.models import User
from src.db.repositories.user_repository import UserRepository

from src.shared.pydantic_schemas.user import UserBase, UserGet, UserExtendedSchema


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def update(self, user_id: int, new_data: UserBase) -> UserGet:
        data_dict = new_data.model_dump()
        new_user_data =  await self.repository.update_one(user_id, data_dict)
        return new_user_data

    async def get_user_by_id(self, user_id: int) -> UserBase:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        return user

    async def deactivate_account(self, user_id: int, status: bool = False):
        deleted_user_data = await self.repository.update_one(user_id, {'is_active': status})
        return deleted_user_data

    async def get_user_with_role(self, user_id: int) -> UserExtendedSchema:
        user = await self.repository.get_with_relationships(user_id)
        if user is None:
            raise ValueError("User not found")
        user_schema = UserExtendedSchema.model_validate(user)
        return user_schema


    async def get_all_users(self) -> List[User]:
        users = await self.repository.get_all()
        return users

    async def change_user_role(self, user_id: int, role_id: int):
        new_user_data = await self.repository.update_one(user_id, {'role_id': role_id})
        return new_user_data
