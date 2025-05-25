from fastapi import HTTPException, Depends, status
from sqlmodel import Session

from mjc.model.entity.course import ClassRole
from mjc.model.schema.user import UserInDB
from mjc.service import course as course_service
from mjc.service.user import get_current_user


async def verify_admin(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not system admin")


def verify_class_admin(db: Session, class_id: int, current_user: UserInDB):
    if  current_user.is_admin:
        return
    role = verify_user_in_class(db, class_id, current_user.username)
    if role is None or ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission")


def verify_user_in_class(db: Session, class_id: int, username: str):
    print(username, class_id)
    role = course_service.get_user_class_role(db, username, class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    return role
