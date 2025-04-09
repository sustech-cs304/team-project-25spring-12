from sqlmodel import Session

from ..model.schema.widget import DocWidgetCreate, DocWidgetUpdate
from ..model.schema.widget import AssignmentWidgetCreate, AssignmentWidgetUpdate
from ..model.schema.widget import NotePdfWidgetCreate, NotePdfWidgetUpdate
from ..model.entity import Widget


def get_widget(session: Session, widget_id: int) -> Widget:
    pass


def create_doc_widget(db: Session, widget: DocWidgetCreate) -> Widget:
    pass


def update_doc_widget(db: Session, widget: DocWidgetUpdate) -> Widget:
    pass


def create_assignment_widget(db: Session, widget: AssignmentWidgetCreate) -> Widget:
    pass


def update_assignment_widget(db: Session, widget: AssignmentWidgetUpdate) -> Widget:
    pass


def create_note_pdf_widget(db: Session, widget: NotePdfWidgetCreate) -> Widget:
    pass


def update_note_pdf_widget(db: Session, widget: NotePdfWidgetUpdate) -> None:
    pass


def delete_widget(db: Session, widget_id: int) -> Widget:
    pass