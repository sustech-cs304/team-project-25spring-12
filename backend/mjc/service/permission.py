from fastapi import Depends
from sqlmodel import Session

from backend.mjc.utils import database
from backend.mjc.model.schema.user import UserInDB
from backend.mjc.service.user import get_current_user


async def class_read(db: Session = Depends(database.get_session),
                     current_user: UserInDB = Depends(get_current_user),
                     ) -> UserInDB:
    pass


async def class_write():
    pass