from fastapi import HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlmodel import Session

import backend.mjc.model.schema.user
from ..crud import user as crud
from ..model import entities
from ..utils import security, database
from .. import config


def pack_profile(user: entities.User) -> backend.mjc.model.schema.user.Profile:
    return backend.mjc.model.schema.user.Profile(
        username=user.username,
        name=user.profile.name,
        department=user.profile.department,
        email=user.profile.email,
        is_active=user.is_active,
        is_admin=user.is_admin
    )


def login(db: Session, username: str, plain_password: str) -> backend.mjc.model.schema.user.Token | None:
    """
    生成 access token.
    :param db: SQLAlchemy.Session
    :param username
    :param plain_password:
    :return: access_token if verified, None otherwise
    """
    user: entities.User = crud.get_user(db, username)
    if user:
        if not user.is_active:
            raise HTTPException(status_code=400, detail="未激活的用户")
        if security.verify_password(plain_password, user.encoded_password):
            return backend.mjc.model.schema.user.Token(access_token=security.generate_access_jwt(username, config.TOKEN_EXPIRE_MINUTES))
    return None


def register(db: Session, user: backend.mjc.model.schema.user.UserCreate) -> backend.mjc.model.schema.user.Profile | None:
    """
    注册用户.
    :param db:
    :param user:
    :return:
    """
    user = crud.create_user(db, user)
    return pack_profile(user)


def get_profile(db: Session, username: str) -> backend.mjc.model.schema.user.Profile | None:
    """
    获取用户资料
    :param db:
    :param username:
    :return:
    """
    user: entities.User = crud.get_user(db, username)
    if user:
        return pack_profile(user)
    return None


@cache(expire=2)
async def get_current_user(db: database.Session,
                           token: str = Depends(security.oauth2_scheme)) -> backend.mjc.model.schema.user.UserInDB:
    """
    For get current authenticated user
    :param db:
    :param token:
    :return:
    """
    username = security.extract_username(token)
    user: entities.User = crud.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="未认证")
    return backend.mjc.model.schema.user.UserInDB.model_validate(user)
