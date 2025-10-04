from sqlalchemy import select

from src.config import async_session
from src.db.models import Role, User
from src.shared.enum_classes.roles import RoleEnum
from src.shared.security.auth import hash_password


async def init_db():
    async with async_session() as db:
        role_result = await db.execute(select(Role))
        roles_exist = role_result.scalars().first() is not None

        if not roles_exist:
            roles = [
                Role(title=RoleEnum.admin.value, access_to_protected_resources=True),
                Role(title=RoleEnum.superuser.value, access_to_protected_resources=True),
                Role(title=RoleEnum.user.value, access_to_protected_resources=False),
            ]
            db.add_all(roles)
            await db.commit()

        user_result = await db.execute(select(User))
        users_exist = user_result.scalars().first() is not None
        if not users_exist:
            admin_role_result = await db.execute(
                select(Role.id).where(Role.title == RoleEnum.admin.value)
            )
            admin_role_id = admin_role_result.scalar_one()

            superuser_role_result = await db.execute(
                select(Role.id).where(Role.title == RoleEnum.superuser.value)
            )
            superuser_role_id = superuser_role_result.scalar_one()

            user_role_result = await db.execute(
                select(Role.id).where(Role.title == RoleEnum.user.value)
            )

            user_role_id = user_role_result.scalar_one()

            admin_user = User(
                email="admin@mail.ru",
                first_name="Admin",
                hashed_password= await hash_password("admin"),
                role_id=admin_role_id,
            )

            superuser_user = User(
                email="superuser@mail.ru",
                first_name="superuser",
                hashed_password= await hash_password("superuser"),
                role_id=superuser_role_id,
            )

            user_user = User(
                email="user@mail.ru",
                first_name="user",
                hashed_password= await hash_password("user"),
                role_id=user_role_id,
            )
            db.add_all([user_user, superuser_user, admin_user])
            await db.commit()
