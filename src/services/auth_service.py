from src.db.repositories.user_repository import UserRepository
from src.services.role_service import RoleService
from src.shared.pydantic_schemas.auth import LoginResponse, RegisterResponse
from src.shared.pydantic_schemas.user import UserLogin, UserCreate
from src.shared.security.auth import verify_password, hash_password
from src.shared.security.jwt import create_access_token, create_refresh_token, decode_token


class AuthService:
    def __init__(self, repository: UserRepository, role_service: RoleService):
        self.repository = repository
        self.role_service = role_service

    @staticmethod
    async def refresh(refresh_token: str):
        payload = await decode_token(refresh_token)
        if payload is None:
            raise ValueError("Invalid Token")
        user_id = payload.get('user_id')
        access_token = await create_access_token({'user_id': user_id})
        return access_token

    async def register(self, user_data: UserCreate) -> RegisterResponse:
        hashed_password = await hash_password(user_data.password)

        user_dict = user_data.model_dump(exclude={'password_confirm', 'password'})
        user_dict['hashed_password'] = hashed_password
        user_role_id = await self.role_service.get_user_role_id()
        new_user_id = await self.repository.add_one(user_dict, user_role_id)

        access_token = await create_access_token({'user_id': new_user_id})
        refresh_token = await create_refresh_token({'user_id': new_user_id})
        return RegisterResponse(
            user_id=new_user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def login(self, login_data: UserLogin) -> LoginResponse:
        user_data = await self.repository.get_by_email(login_data.email)

        if user_data is None:
            raise ValueError("User with inputted email not found")

        is_valid_password = await verify_password(user_data.hashed_password, login_data.password)

        if not is_valid_password:
            raise ValueError("Incorrect password")

        access_token = await create_access_token({'user_id': user_data.id})
        refresh_token = await create_refresh_token({'user_id': user_data.id})

        return LoginResponse(
            user=user_data,
            access_token=access_token,
            refresh_token=refresh_token
        )

