from fastapi import HTTPException, status
from sqlmodel import Session

from backend.mjc.crud import folder as folder_crud, page as page_crud
from backend.mjc.crud.course import get_class, get_user_class_role
from backend.mjc.model.schema.folder import Folder, FolderUpdate
from backend.mjc.model.schema.user import UserInDB
from model.entity import ClassRole, Folder as FolderEntity
from model.schema.folder import FolderPageItem, FolderCreate


def entity2folder(entity: FolderEntity) -> Folder:
    return Folder(pages=[FolderPageItem.model_validate(page.model_dump()) for page in entity.pages],
                  **entity.model_dump())

def get_folder(db: Session, folder_id: int) -> Folder:
    return folder_crud.get_folder(db, folder_id)


def get_class_folders(db: Session, class_id: int, visible: bool = None) -> list[Folder]:
    folder_entities = folder_crud.get_class_folders(db, class_id)
    folders: list[Folder] = []
    for folder_entity in folder_entities:
        if folder_entity.visible == visible:
            folder = Folder(
                **folder_entity.model_dump(),
                pages=[FolderPageItem.model_validate(page.model_dump()) for page in folder_entity.pages
                       if page.visible or visible is None]  # 有 visible 的判断条件，或者全部都可见
                                                            # 注意到此处 visible 的判断条件是 folder - page 传递的
            )
            folders.append(folder)
    return folders


def get_uncategorized_folder(db: Session, class_id: int, visible: bool = None) -> Folder:
    pages = page_crud.get_get_uncategorized_pages(db, class_id)
    folder = Folder(
        name='Uncategorized', index=998244353, pages=[
            FolderPageItem.model_validate(page.model_dump()) for page in pages
            if page.visible or visible is None
        ]
    )
    return folder


def get_user_class_folders(db: Session, class_id: int, user: UserInDB) -> list[Folder]:
    role = get_user_class_role(db, user.username, class_id)
    if role is ClassRole.STUDENT:
        folders = get_class_folders(db, class_id, visible=True)
        uncategorized_folder = get_uncategorized_folder(db, class_id, visible=True)
        uncategorized_folder.index = len(folders)
        folders.append(uncategorized_folder)
    else:
        folders = get_class_folders(db, class_id)
        uncategorized_folder = get_uncategorized_folder(db, class_id, visible=True)
        uncategorized_folder.index = len(folders)
        folders.append(uncategorized_folder)
    return sorted(folders, key=lambda folder: folder.index)


def create_folder(db: Session, folder: FolderCreate) -> Folder:
    folder_entity = folder_crud.create_folder(db, folder)
    return entity2folder(folder_entity)


def update_folder(db: Session, folder: FolderUpdate) -> Folder:
    folder_entity = folder_crud.update_folder(db, folder)
    return entity2folder(folder_entity)


def delete_folder(db: Session, folder_id: int):
    folder = get_folder(db, folder_id)
    if folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Folder not found')
    folder_crud.delete_folder(db, folder_id)