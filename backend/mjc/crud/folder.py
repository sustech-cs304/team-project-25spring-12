from sqlmodel import Session, select

from ..model.entity import Folder, Page
from ..model.schema.folder import FolderCreate, FolderUpdate


def get_class_folders(db: Session, class_id: int) -> list[Folder]:
    stmt = select(Folder).where(Folder.id == class_id).where(Folder.is_deleted == False)
    folders: list[Folder] = db.exec(stmt).all()
    return folders


def create_folder(db: Session, folder: FolderCreate) -> Folder:
    folder_entity = Folder(
        name=folder.name,
        index=folder.index,
        class_id=folder.class_id
    )
    db.add(folder_entity)
    db.refresh(folder_entity)
    # 将页面按顺序加入到文件夹中
    for i, page_id in enumerate(folder.order):
        stmt = select(Page).where(Page.id == page_id).where(Page.is_deleted == False)
        page: Page = db.exec(stmt).first()
        if page:
            page.folder = folder_entity
            page.index = i
    return folder_entity



def update_folder(db: Session, folder: FolderUpdate) -> Folder:
    pass


def delete_folder(db: Session, folder_id: int) -> Folder:
    pass