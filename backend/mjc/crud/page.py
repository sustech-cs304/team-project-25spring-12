from sqlmodel import Session, select

from backend.mjc.model.entity import Page, Widget
from backend.mjc.model.schema.page import PageCreate, PageUpdate


def update_widget_order(db: Session, order: list[int]):
    for i, widget_id in enumerate(order):
        stmt = select(Page).where(Widget.id == widget_id).where(Widget.is_deleted == False)
        widget: Widget = db.exec(stmt).first()
        if widget:
            widget.index = i


def get_page(db: Session, page_id: int) -> Page:
    stmt = select(Page).where(Page.id == page_id).where(Page.is_deleted == False)
    page: Page = db.exec(stmt).first()
    return page


def get_class_pages(db: Session, class_id: int) -> list[Page]:
    stmt = select(Page).where(Page.class_id == class_id).where(Page.is_deleted == False)
    pages: list[Page] = db.exec(stmt).all()
    return pages


def get_get_uncategorized_pages(db: Session, class_id: int) -> list[Page]:
    stmt = select(Page).where(Page.class_id == class_id) \
                       .where(Page.is_deleted == False) \
                       .where(Page.folder_id == None)
    pages = db.exec(stmt).all()
    return pages


def create_page(db: Session, page: PageCreate) -> Page:
    page_entity: Page = Page(
        name=page.name,
        class_id=page.class_id,
        folder_id=page.folder_id,
        index=page.index,
        visible=page.visible
    )
    db.add(page_entity)
    db.commit()
    db.refresh(page_entity)
    return page_entity


def update_page(db: Session, page: PageUpdate) -> Page:
    stmt = select(Page).where(Page.id == page.id).where(Page.is_deleted == False)
    page_entity: Page = db.exec(stmt).first()
    if page_entity:
        page_entity.name = page.name
        page_entity.folder_id = page.folder_id
        page_entity.visible = page.visible
        if page.order:
            update_widget_order(db, page.order)
    db.commit()
    return page_entity


def delete_page(db: Session, page_id: int) -> Page:
    stmt = select(Page).where(Page.id == page_id).where(Page.is_deleted == False)
    page: Page = db.exec(stmt).first()
    if page:
        for widget in page.widgets:
            widget.is_deleted = True
        page.is_deleted = True
        db.refresh(page)
    db.commit()
    return page