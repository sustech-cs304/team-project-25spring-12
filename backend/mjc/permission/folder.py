from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.model.schema.folder import FolderCreate, FolderUpdate
from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.service.user import get_current_user
from mjc.service import course as course_service, folder as folder_service
from mjc.permission.common import verify_class_admin


def verify_folder_exist(db: Session, folder_id: int):
    folder = folder_service.get_folder(db, folder_id)
    if folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return folder


async def verify_folders_get(db: SessionDep, class_id: int,
                            current_user: UserInDB = Depends(get_current_user)):
    role = course_service.get_user_class_role(db, current_user.username, class_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this class")


async def verify_folder_create(db: SessionDep, request: FolderCreate,
                               current_user: UserInDB = Depends(get_current_user)):
    verify_class_admin(db, request.class_id, current_user)


async def verify_folder_update(db: SessionDep, request: FolderUpdate,
                               current_user: UserInDB = Depends(get_current_user)):
    folder = verify_folder_exist(db, request.id)
    verify_class_admin(db, folder.class_id, current_user)


async def verify_folder_delete(db: SessionDep, folder_id: int,
                               current_user: UserInDB = Depends(get_current_user)):
    folder = verify_folder_exist(db, folder_id)
    verify_class_admin(db, folder.class_id, current_user)
