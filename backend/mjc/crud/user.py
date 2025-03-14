from sqlmodel import Session, select

from ..model.entities import User
from ..model.schemas import UserCreate


def get_user(db: Session, username: str) -> User:
    stmt = select(User).where(User.username == username)
    return db.exec(stmt).first()