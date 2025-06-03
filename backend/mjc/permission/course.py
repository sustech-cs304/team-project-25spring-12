from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.model.entity.course import ClassRole
from mjc.service.user import get_current_user
from mjc.service import course as course_service
from mjc.model.schema.course import ClassUpdate


def verify_class_exist(db: SessionDep, class_id: int):
    if course_service.get_class(db, class_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")


def verify_admin(current_user: UserInDB):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not system admin")


async def verify_semester_class_get(semester_id: int,
                                    current_user: UserInDB = Depends(get_current_user)):
    verify_admin(current_user)


async def verify_class_get(db: SessionDep,
                           class_id: int,
                           current_user: UserInDB = Depends(get_current_user)):
    verify_class_exist(db, class_id)
    role = course_service.get_user_class_role(db, current_user.username, class_id)
    if role is None and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in the class")


async def verify_class_create(current_user: UserInDB = Depends(get_current_user)):
    verify_admin(current_user)


async def verify_class_update(db: SessionDep,
                              cls: ClassUpdate,
                              current_user: UserInDB = Depends(get_current_user)):
    verify_class_exist(db, cls.id)
    role = course_service.get_user_class_role(db, current_user.username, cls.id)
    if (role is None and not current_user.is_admin) or role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission")


async def verify_class_delete(db: SessionDep,
                              class_id: int,
                              current_user: UserInDB = Depends(get_current_user)):
    verify_class_exist(db, class_id)
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not system admin")