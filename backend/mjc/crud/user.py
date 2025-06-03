from sqlmodel import Session, select

from mjc.model.entity.user import User, Profile
from mjc.model.schema.user import UserCreate, ChangePassword
from mjc.utils import security


def get_user(db: Session, username: str) -> User:
    """
    获取用户。
    :param db: 传入的 database Session
    :param username: 查找的用户名
    :return: 用户实体
    """
    stmt = select(User).where(User.username == username)
    return db.exec(stmt).first()


def get_profile_fuzz(db: Session, username: str | None, department: str | None, email: str | None,
                     limit: int = 10, offset: int = 0) -> list[Profile]:
    stmt = select(Profile)
    if username:
        stmt = stmt.where(Profile.username.like(f'%{username}%'))
    if department:
        stmt = stmt.where(Profile.department.like(f'%{department}%'))
    if email:
        stmt = stmt.where(Profile.department.like(f'%{email}%'))
    stmt = stmt.offset(offset).limit(limit)
    return db.exec(stmt).all()


def get_profile(db: Session, username: str) -> Profile:
    stmt = select(Profile).where(Profile.username == username)
    return db.exec(stmt).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    创建新用户。
    :param db: 传入的 database Session
    :param user: 新建用户的信息
    :return: 用户实体
    """
    user_entity = User(username=user.username, encoded_password=security.encode_password(user.password))
    profile_entity = Profile(username=user.username,
                             name=user.name,
                             department=user.department,
                             email=user.email)
    db.add(user_entity)
    db.add(profile_entity)
    db.commit()
    db.refresh(user_entity)
    return user_entity


def change_password(db: Session, username: str, request: ChangePassword) -> User:
    """
    修改密码
    :param db:
    :param username:
    :param request:
    :return:
    """
    # 注意到此处不包含原始密码校验。该校验需要放到 service 层处理。
    user = get_user(db, username=username)
    user.password = security.encode_password(request.new_password)
    db.commit()
    db.refresh(user)
    return user
