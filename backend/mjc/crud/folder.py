from sqlmodel import Session, select

from mjc.model.entity import Folder, Page
from mjc.model.schema.folder import FolderCreate, FolderUpdate


def update_page_order(db: Session, order: list[int], folder: Folder):
    """
    将页面按顺序加入到文件夹中
    """
    for i, page_id in enumerate(order):
        stmt = select(Page).where(Page.id == page_id).where(Page.is_deleted == False)
        page: Page = db.exec(stmt).first()
        if page:
            page.folder = folder
            page.index = i


def get_class_folders(db: Session, class_id: int, ) -> list[Folder]:
    stmt = select(Folder).where(Folder.id == class_id) \
                         .where(Folder.is_deleted == False)
    folders: list[Folder] = db.exec(stmt).all()
    return folders


def get_folder(db: Session, folder_id: int) -> Folder:
    stmt = select(Folder).where(Folder.id == folder_id).where(Folder.is_deleted == False)
    folder: Folder = db.exec(stmt).first()
    return folder


def create_folder(db: Session, folder: FolderCreate) -> Folder:
    folder_entity = Folder(
        name=folder.name,
        index=folder.index,
        class_id=folder.class_id,
        visible=folder.visible
    )
    db.add(folder_entity)
    db.commit()
    db.refresh(folder_entity)
    if folder.order:
        update_page_order(db, folder.order, folder_entity)
    return folder_entity


def update_folder(db: Session, folder: FolderUpdate) -> Folder:
    stmt = select(Folder).where(Folder.id == folder.id).where(Folder.is_deleted == False)
    folder_entity: Folder = db.exec(stmt).first()
    if folder:
        folder_entity.name = folder.name
        folder.visible = folder.visible
        if folder.order:
            update_page_order(db, folder.order, folder_entity)
    db.commit()
    return folder_entity


def delete_folder(db: Session, folder_id: int) -> Folder:
    stmt = select(Folder).where(Folder.id == folder_id).where(Folder.is_deleted == False)
    folder: Folder = db.exec(stmt).first()
    if folder:
        for page in folder.pages:
            page.folder_id = None
        folder.is_deleted = True
    db.commit()
    return folder