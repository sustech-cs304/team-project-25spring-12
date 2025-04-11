from fastapi import HTTPException, status
from sqlmodel import Session

from backend.mjc.crud import folder as folder_crud, page as page_crud
from backend.mjc.crud.course import get_class, get_user_class_role
from backend.mjc.model.schema.folder import Folder, FolderUpdate
from backend.mjc.model.schema.user import UserInDB
from model.entity import ClassRole
from model.schema.folder import FolderPageItem, FolderCreate


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
    cls = get_class(db, class_id)
    if not cls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Class not found')
    role = get_user_class_role(db, user.username, class_id)
    if role is None and not user.is_admin:  # 管理员也可以得到这个
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User has not enrolled')

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


def create_folder(db: Session, folder: FolderCreate, user: UserInDB) -> Folder:
    folder_crud.create_folder(db, folder)


def update_folder(db: Session, folder: FolderUpdate, user: UserInDB) -> Folder:
    pass


def delete_folder(db: Session, folder_id: int, user: UserInDB) -> Folder:
    pass