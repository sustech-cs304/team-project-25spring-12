from fastapi import APIRouter, Depends

from mjc.utils.database import SessionDep
from mjc.service import folder as folder_service
from mjc.service.user import get_current_user
from mjc.model.schema.folder import FolderCreate, FolderUpdate
from mjc.model.schema.user import UserInDB

router = APIRouter()


@router.get('/class/{class_id}/folder')
async def get_class_folders(db: SessionDep, class_id: int,
                            current_user: UserInDB = Depends(get_current_user)):
    return folder_service.get_user_class_folders(db, class_id, current_user)


@router.post('/class/folder')
async def create_class_folder(db: SessionDep, folder: FolderCreate,
                              current_user: UserInDB = Depends(get_current_user)):
    return folder_service.create_folder(db, folder)


@router.patch('/class/folder')
async def update_folder(db: SessionDep, folder: FolderUpdate,
                        current_user: UserInDB = Depends(get_current_user)):
    return folder_service.update_folder(db, folder)


@router.delete('/class/folder/{folder_id}')
async def delete_folder(db: SessionDep, folder_id: int):
    return folder_service.delete_folder(db, folder_id)