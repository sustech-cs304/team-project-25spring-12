from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.model.schema.page import PageCreate, PageUpdate
from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.model.entity.course import ClassRole
from mjc.service.user import get_current_user
from mjc.service import page as page_service, course as course_service
from mjc.model.schema.course import ClassUpdate
from mjc.crud import page as crud_page


def verify_page_exist(db: Session, page_id: int):
    if crud_page.get_page(db, page_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")


async def verify_page_get(db: SessionDep, page_id: int,
                    current_user: UserInDB = Depends(get_current_user)):
    page = crud_page.get_page(db, page_id)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    role = course_service.get_user_class_role(db, current_user.username, page.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        if page.visible is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission")


async def verify_page_create(db: SessionDep,
                       request: PageCreate,
                       current_user: UserInDB = Depends(get_current_user)):
    role = course_service.get_user_class_role(db, current_user.username, request.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission")


async def verify_page_update(db:SessionDep,
                       request: PageUpdate,
                       current_user: UserInDB = Depends(get_current_user)):
    page = crud_page.get_page(db, request.page_id)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    role = course_service.get_user_class_role(db, current_user.username, page.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission")


async def verify_page_delete(db: SessionDep, page_id: int,
                       current_user: UserInDB = Depends(get_current_user)):
    verify_page_exist(db, page_id)
    page = crud_page.get_page(db, page_id)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    role = course_service.get_user_class_role(db, current_user.username, page.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission")
