from src.db.repositories.role_repository import RoleRepository
from src.shared.pydantic_schemas.role import Rights


class RoleService:
    def __init__(self, repository: RoleRepository):
       self.repository = repository

    async def get_user_role_id(self) -> int | None:
        role_id = await self.repository.get_user_role_id()
        if role_id is None:
            role_id = await self.repository.create_user_role()
        return role_id

    async def update_role(self, role_id: int, new_rights: Rights):
        role = await self.repository.update_rights(role_id, new_rights)
        if role is None:
            raise ValueError("Role not found")
        return role


