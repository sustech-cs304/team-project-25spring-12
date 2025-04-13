from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from backend.mjc import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bad_credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, encoded_password: str) -> bool:
    """
    通过 HS256 验证密码.
    :param plain_password: 前端传进的原始密码
    :param encoded_password: 数据库中加密的密码
    :return:
    """
    return pwd_context.verify(plain_password, encoded_password)


def encode_password(password: str | bytes) -> str:
    """
    通过 HS256 加密密码.
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def generate_jwt(data: dict, expires_delta: timedelta | None) -> str:
    """
    通过给定的 JWT payload `data` 和生存周期生成 JWT.
    :param data: JWT payload
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ENCODE_ALGORITHM)
    return encoded_jwt


def generate_access_jwt(username: str, expires_delta: timedelta | None = None):
    """
    通过 Service 层中的 login() 调用
    :param username: 用户名
    :param expires_delta:
    :return:
    """
    return generate_jwt(data={"sub": username}, expires_delta=expires_delta)


def extract_payloads(token: str) -> dict:
    """
    提取 JWT payload.
    :param token: JWT
    :return:
    """
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ENCODE_ALGORITHM])
    return payload


def extract_username(token: str) -> str | None:
    """
    提取 JWT 中的 username 项.
    :param token: JWT
    :return:
    """
    try:
        payload = extract_payloads(token)
    except JWTError as e:
        return None
    return payload.get("sub")