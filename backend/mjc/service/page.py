from fastapi import HTTPException, status
from sqlmodel import Session

from backend.mjc.model.schema.common import Message
from backend.mjc.model.schema.page import Page, PageCreate, PageUpdate
from backend.mjc.model.entity import Page as PageEntity, WidgetType
from backend.mjc.crud import page as crud_page
from backend.mjc.service import widget as widget_service


def entity2page(entity: PageEntity) -> Page:
    page = Page(id=entity.id,
                name=entity.name,
                index=entity.index,
                visible=entity.visible,
                widgets=[widget_service.entity2widget(widget) for widget in entity.widgets if widget and widget.is_deleted == False])
    return page


def get_page(db: Session, page_id: int) -> Page | None:
    page = crud_page.get_page(db, page_id)
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    return entity2page(page)


def create_page(db: Session, page_create: PageCreate) -> Page :
    page = crud_page.create_page(db, page_create)
    if not page:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create page failed")
    return entity2page(page)


def update_page(db: Session, page_update: PageUpdate) -> Page:
    page = crud_page.update_page(db, page_update)
    if not page:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update page failed")
    return entity2page(page)


def delete_page(db: Session, page_id: int) -> Message:
    page = crud_page.delete_page(db, page_id)
    if page:
        return Message(msg="Page deleted successfully")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete page failed")
