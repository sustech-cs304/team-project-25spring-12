from typing import Generator, Annotated

from fastapi.params import Depends
from sqlmodel import Session, SQLModel

from ..model.database import engine
from ..model import entities  # 通过引用 entities.py 中定义的数据库实体来初始化 metadata


def get_session() -> Generator[Session, None, None]:
    """
    为一个请求获得一个数据库 Session 的 Generator (异步)
    :return:
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    根据 SQLModel 定义的 metadata 创建并初始化数据库.
    :return:
    """
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]