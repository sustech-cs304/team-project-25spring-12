from fastapi import HTTPException
from sqlmodel import Session

from backend.mjc.crud import folder as folder_crud
from backend.mjc.crud.course import get_user_class_role
from backend.mjc.model.schema.folder import Folder
from model.schema.user import UserInDB


def get_class_folders(db: Session, class_id: int) -> list[Folder]:
    pass


def get_user_class_folders(db: Session, class_id: int, user: UserInDB) -> list[Folder]:
    pass


def create_folder(db: Session, folder: Folder, user: UserInDB) -> Folder:
    pass


def update_folder(db: Session, folder_id: int, folder: Folder, user: UserInDB) -> Folder:
    pass


def delete_folder(db: Session, folder_id: int, user: User) -> Folder:
    pass