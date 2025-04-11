from fastapi import HTTPException, status
from sqlmodel import Session

from backend.mjc.crud import widget as crud_widget
from backend.mjc.model.schema.user import UserInDB
from backend.mjc.model.schema.widget import AssignmentWidget, NotePdfWidget, DocWidget, DocWidgetCreate, \
    DocWidgetUpdate, \
    AssignmentWidgetCreate, AssignmentWidgetUpdate, NotePdfWidgetCreate, NotePdfWidgetUpdate, WidgetAttachmentCreate
from backend.mjc.model.entity import Widget as WidgetEntity, WidgetType


def entity2widget(entity: WidgetEntity) -> AssignmentWidget | NotePdfWidget | DocWidget | None:
    if entity.type == WidgetType.doc:
        doc_widget = DocWidget.model_validate(entity.model_dump())
        return doc_widget
    elif entity.type == WidgetType.assignment:
        assignment_widget = AssignmentWidget.model_validate(**entity.assignment_widget.model_dump())
        return assignment_widget
    elif entity.type == WidgetType.note_pdf:
        return NotePdfWidget.model_validate(**entity.note_pdf_widget.model_dump())


def create_doc_widget(db: Session, editor: UserInDB, doc_widget_create: DocWidgetCreate) -> DocWidget:
    widget_entity = crud_widget.create_doc_widget(db, doc_widget_create, editor)
    if widget_entity:
        doc_widget = entity2widget(widget_entity)
        return doc_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create doc widget failed")


def update_doc_widget(db:Session, editor: UserInDB, doc_widget_update: DocWidgetUpdate) -> DocWidget:
    widget_entity = crud_widget.update_doc_widget(db, doc_widget_update, editor)
    if widget_entity:
        doc_widget = entity2widget(widget_entity)
        return doc_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update doc widget failed")


def create_assignment_widget(db:Session, editor:UserInDB, assignment_widget_create: AssignmentWidgetCreate) -> AssignmentWidget:
    widget_entity = crud_widget.create_assignment_widget(db, assignment_widget_create, editor)
    if widget_entity:
        assignment_widget = entity2widget(widget_entity)
        return assignment_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create assignment widget failed")


def update_assignment_widget(db:Session, editor: UserInDB, assignment_widget_update: AssignmentWidgetUpdate) -> AssignmentWidget:
    widget_entity = crud_widget.update_assignment_widget(db, assignment_widget_update, editor)
    if widget_entity:
        assignment_widget = entity2widget(widget_entity)
        return assignment_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update assignment widget failed")


def create_note_pdf_widget(db:Session, editor:UserInDB, note_pdf_widget_create: NotePdfWidgetCreate) -> NotePdfWidget:
    widget_entity = crud_widget.create_note_pdf_widget(db, note_pdf_widget_create, editor)
    if widget_entity:
        note_pdf_widget = entity2widget(widget_entity)
        return note_pdf_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create note pdf widget failed")


def update_note_pdf_widget(db: Session, editor:UserInDB, note_pdf_widget_update: NotePdfWidgetUpdate) -> NotePdfWidget:
    widget_entity = crud_widget.update_widget(db, note_pdf_widget_update,editor)
    if widget_entity:
        note_pdf_widget = entity2widget(widget_entity)
        return note_pdf_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update note pdf widget failed")


def delete_widget(db: Session, widget_id: int):
    widget_entity = crud_widget.delete_widget(db, widget_id)
    if widget_entity:
        return widget_entity
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete widget failed")


def add_widget_attachment(db:Session, attachment: WidgetAttachmentCreate) -> DocWidget | AssignmentWidget | NotePdfWidget:
    # TODO:
    pass


def delete_attachment(db:Session, attachment_id: int):
    attachment_entity = crud_widget.delete_widget(db, attachment_id)
    if attachment_entity:
        return attachment_entity
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete attachment failed")
