from fastapi import HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlmodel import Session

from mjc.crud import user as crud
from mjc.model.entity.user import User, Profile as ProfileEntity
from mjc.model.schema.user import UserInDB, Token, Profile, UserCreate
from mjc.utils import security, database
from mjc import config


def entity2profile(entity: ProfileEntity) -> Profile:
    return Profile(
        **entity.model_dump(),
        is_admin=entity.user.is_admin,
        is_active=entity.user.is_active
    )


def pack_profile(user: User) -> Profile:
    return Profile(
        username=user.username,
        name=user.profile.name,
        department=user.profile.department,
        email=user.profile.email,
        is_active=user.is_active,
        is_admin=user.is_admin
    )


def login(db: Session, username: str, plain_password: str) -> Token | None:
    """
    生成 access token.
    :param db: SQLAlchemy.Session
    :param username
    :param plain_password:
    :return: access_token if verified, None otherwise
    """
    user: User = crud.get_user(db, username)
    if user:
        if not user.is_active:
            raise HTTPException(status_code=400, detail="未激活的用户")
        if security.verify_password(plain_password, user.encoded_password):
            return Token(access_token=security.generate_access_jwt(username, config.TOKEN_EXPIRE_MINUTES))
    return None


def register(db: Session, user: UserCreate) -> Profile | None:
    """
    注册用户.
    :param db:
    :param user:
    :return:
    """
    user = crud.create_user(db, user)
    return pack_profile(user)


def get_profile(db: Session, username: str) -> Profile | None:
    """
    获取用户资料
    :param db:
    :param username:
    :return:
    """
    user: User = crud.get_user(db, username)
    if user:
        return pack_profile(user)
    return None


def get_profile_fuzz(db: Session, username: str | None, department: str | None, email: str | None,
                     limit: int = 10, offset: int = 0) -> list[Profile] | None:
    profiles = crud.get_profile_fuzz(db, username, department, email, limit, offset)
    if profiles:
        return [Profile.model_validate(profile.model_dump()) for profile in profiles]
    return []


@cache(expire=2)
async def get_current_user(db: Session = Depends(database.get_session),
                           token: str = Depends(security.oauth2_scheme)) \
        -> UserInDB:
    """
    For get current authenticated user
    :param db:
    :param token:
    :return:
    """
    username = security.extract_username(token)
    user: User = crud.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return UserInDB.model_validate(user.model_dump())
