from datetime import timedelta, timezone, datetime

from jose import jwt, JWTError

from src.config import get_jwt_data


async def create_access_token(data: dict):
    jwt_data = await get_jwt_data()
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_data["expire_access"])
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "access"})
    encode_jwt = jwt.encode(to_encode, jwt_data['secret_key'], algorithm=jwt_data['algorithm'])
    return encode_jwt

async def create_refresh_token(data: dict):
    jwt_data = await get_jwt_data()
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_data["expire_refresh"])
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    encode_jwt = jwt.encode(to_encode, jwt_data['secret_key'], algorithm=jwt_data['algorithm'])
    return encode_jwt


async def decode_token(token: str):
    jwt_data = await get_jwt_data()
    try:
        payload = jwt.decode(token, jwt_data['secret_key'], algorithms=jwt_data['algorithm'])
        return payload
    except JWTError:
        return None