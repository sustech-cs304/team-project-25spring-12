from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.model.schema.folder import FolderCreate, FolderUpdate
from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.model.entity.course import ClassRole
from mjc.service.user import get_current_user
from mjc.service import course as course_service, folder as folder_service


def verify_folder_exist(db: Session, folder_id: int):
    if folder_service.get_folder(db, folder_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")


async def verify_folders_get(db: SessionDep, class_id: int,
                            current_user: UserInDB = Depends(get_current_user)):
    role = course_service.get_user_class_role(db, current_user.username, class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")


async def verify_folder_create(db: SessionDep, request: FolderCreate,
                               current_user: UserInDB = Depends(get_current_user)):
    role = course_service.get_user_class_role(db, current_user.username, request.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission")


async def verify_folder_update(db: SessionDep, request: FolderUpdate,
                               current_user: UserInDB = Depends(get_current_user)):
    verify_folder_exist(db, request.id)
    folder = folder_service.get_folder(db, request.id)
    role = course_service.get_user_class_role(db, current_user.username, folder.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission")


async def verify_folder_delete(db: SessionDep, folder_id: int,
                               current_user: UserInDB = Depends(get_current_user)):
    verify_folder_exist(db, folder_id)
    folder = folder_service.get_folder(db, folder_id)
    role = course_service.get_user_class_role(db, current_user.username, folder.class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")
    elif role is ClassRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission")
