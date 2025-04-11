from datetime import datetime
from idlelib import editor

from sqlmodel import Session, select

from backend.mjc.model.schema.user import UserInDB
from backend.mjc.model.schema.widget import WidgetAttachmentCreate
from backend.mjc.model.schema.widget import DocWidgetCreate, DocWidgetUpdate
from backend.mjc.model.schema.widget import AssignmentWidgetCreate, AssignmentWidgetUpdate
from backend.mjc.model.schema.widget import NotePdfWidgetCreate, NotePdfWidgetUpdate
from backend.mjc.model.entity import Widget, WidgetType, WidgetAttachment, AssignmentWidget, NotePDFWidget, SubmitType


def get_widget(db: Session, widget_id: int) -> Widget:
    stmt = select(Widget).where(Widget.id == widget_id).where(Widget.is_deleted == False)
    widget: Widget = db.exec(stmt).first()
    return widget


def create_widget(db, widget: DocWidgetCreate | AssignmentWidgetCreate | NotePdfWidgetCreate,
                  editor: UserInDB) \
        -> Widget:
    widget_entity = Widget(
        title=widget.title,
        index=widget.index,
        type=WidgetType[widget.type].value,
        create_time=datetime.now(),
        update_time=datetime.now(),
        editor_username=editor.username,
        content=widget.content,
        page_id=widget.page_id,
        visible=widget.visible
    )
    db.add(widget_entity)
    db.refresh(widget_entity)
    return widget_entity


def update_widget(db: Session,
                  widget: DocWidgetUpdate | AssignmentWidgetUpdate | NotePdfWidgetUpdate,
                  editor: UserInDB) -> Widget:
    widget_entity = get_widget(db, widget.id)
    widget_entity.title = widget.title
    widget_entity.content = widget.content
    widget_entity.editor_username = editor.username
    widget_entity.update_time = datetime.now()
    widget_entity.visible = widget.visible
    db.refresh(widget_entity)
    return widget_entity


def create_widget_attachment(db: Session, widget_attachment: WidgetAttachmentCreate) -> WidgetAttachment:
    attach = WidgetAttachment(
        file_id=widget_attachment.file.id,
        widget_id=widget_attachment.widget_id,
    )
    db.add(attach)
    db.refresh(attach)
    return attach


def delete_widget_attachment(db: Session, file_id: int) -> WidgetAttachment:
    stmt = select(WidgetAttachment).where(WidgetAttachment.file_id == file_id)
    attachment: WidgetAttachment = db.exec(stmt).first()
    if attachment:
        attachment.is_deleted = True
    db.refresh(attachment)
    return attachment


def create_doc_widget(db: Session, widget: DocWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    return widget_entity


def update_doc_widget(db: Session, widget: DocWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    db.refresh(widget)
    return widget_entity


def create_assignment_widget(db: Session, widget: AssignmentWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    assignment = AssignmentWidget(
        widget_id=widget_entity.id,
        submit_type=[SubmitType[typ].value for typ in widget.submit_type],
        ddl=widget.ddl,
        max_score=widget.max_score,
    )
    db.add(assignment)
    db.refresh(widget_entity)
    return widget_entity


def update_assignment_widget(db: Session, widget: AssignmentWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    widget_entity.assignment_widget.submit_type = [SubmitType[typ].value for typ in widget.submit_type]
    widget_entity.assignment_widget.ddl = widget.ddl
    widget_entity.assignment_widget.max_score = widget.max_score
    db.refresh(widget_entity)
    return widget_entity


def create_note_pdf_widget(db: Session, widget: NotePdfWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    note_pdf = NotePDFWidget(
        widget_id=widget_entity.id,
        pdf_file_id=widget.pdf_file.id
    )
    db.add(note_pdf)
    db.refresh(widget_entity)
    return widget_entity


def update_note_pdf_widget(db: Session, widget: NotePdfWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    widget_entity.note_pdf_widget.pdf_file_id = widget.pdf_file.id
    db.refresh(widget_entity)
    return widget_entity


def delete_widget(db: Session, widget_id: int) -> Widget:
    widget_entity = get_widget(db, widget_id)
    if widget_entity:
        widget_entity.is_deleted = True
    db.refresh(widget_entity)
    return widget_entity