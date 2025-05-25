from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.model.schema.page import PageCreate, PageUpdate
from mjc.permission.common import verify_class_admin
from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.model.entity.course import ClassRole
from mjc.service.user import get_current_user
from mjc.service import course as course_service
from mjc.crud import page as crud_page


def verify_page_exist(db: Session, page_id: int):
    page = crud_page.get_page(db, page_id)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    return page


async def verify_page_get(db: SessionDep, page_id: int,
                    current_user: UserInDB = Depends(get_current_user)):
    page = verify_page_exist(db, page_id)
    role = course_service.get_user_class_role(db, current_user.username, page.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        if page.visible is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission")


async def verify_page_create(db: SessionDep,
                       request: PageCreate,
                       current_user: UserInDB = Depends(get_current_user)):
    verify_class_admin(db, request.class_id, current_user)


async def verify_page_update(db:SessionDep,
                       request: PageUpdate,
                       current_user: UserInDB = Depends(get_current_user)):
    verify_page_exist(db, request.id)
    verify_class_admin(db, request.class_id, current_user)


async def verify_page_delete(db: SessionDep, page_id: int,
                       current_user: UserInDB = Depends(get_current_user)):
    page = verify_page_exist(db, page_id)
    verify_class_admin(db, page.class_id, current_user)
