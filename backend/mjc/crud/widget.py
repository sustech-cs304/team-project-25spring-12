from datetime import datetime

from sqlmodel import Session, select

from ..model.schema.user import UserInDB
from ..model.schema.widget import DocWidgetCreate, DocWidgetUpdate
from ..model.schema.widget import AssignmentWidgetCreate, AssignmentWidgetUpdate
from ..model.schema.widget import NotePdfWidgetCreate, NotePdfWidgetUpdate
from ..model.entity import Widget, WidgetType, WidgetAttachment, LocalResourceFile


def get_widget(db: Session, widget_id: int) -> Widget:
    stmt = select(Widget).where(Widget.id == widget_id).where(Widget.is_deleted == False)
    widget: Widget = db.exec(stmt).first()
    return widget


def create_doc_widget(db: Session, widget: DocWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = Widget(
        title=widget.title,
        index=widget.index,
        type=WidgetType.doc,
        create_time=datetime.now(),
        update_time=datetime.now(),
        editor_username=editor.username,
        content=widget.content,
        page_id=widget.page_id,
        visible=widget.visible
    )
    db.add(widget_entity)
    db.refresh(widget_entity)
    for attachment in widget.attachments:
        stmt = select(LocalResourceFile).where(LocalResourceFile.id == attachment.id) \
                                        .where(LocalResourceFile.is_deleted == False)
        file: LocalResourceFile = db.exec(stmt).first()
        if file:
            wid_attach = WidgetAttachment(
                file_id=attachment.id,
                uploader_username=file.uploader_username,
                widget_id=widget_entity.id
            )
            db.add(wid_attach)
            db.refresh(wid_attach)
    db.refresh(widget_entity)
    return widget_entity


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