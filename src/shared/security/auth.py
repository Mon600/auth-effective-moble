from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(hashed_password: str, raw_password: str):
    is_valid_password = pwd_context.verify(raw_password, hashed_password)
    return is_valid_password