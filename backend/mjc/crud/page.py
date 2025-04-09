from sqlmodel import Session

from ..model.entity import Page
from ..model.schema.page import PageCreate, PageUpdate


def get_page(db: Session, page_id: int) -> Page:
    pass


def get_class_pages(db: Session, class_id: int) -> list[Page]:
    pass


def create_page(db: Session, page: PageCreate) -> Page:
    pass


def update_page(db: Session, page: PageUpdate) -> Page:
    pass


def delete_page(db: Session, page_id: int) -> Page:
    pass