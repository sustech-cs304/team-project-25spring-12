import uuid
from datetime import datetime

from sqlmodel import Session, select

from mjc.model.schema.user import UserInDB
from mjc.model.schema.widget import WidgetAttachmentCreate
from mjc.model.schema.widget import DocWidgetCreate, DocWidgetUpdate
from mjc.model.schema.widget import AssignmentWidgetCreate, AssignmentWidgetUpdate
from mjc.model.schema.widget import NotePdfWidgetCreate, NotePdfWidgetUpdate, NoteCreate, NoteUpdate
from mjc.model.entity.widget import Widget, WidgetType, WidgetAttachment, AssignmentWidget, NotePDFWidget, SubmitType, \
    Note


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
        type=WidgetType(widget.type),
        create_time=datetime.now(),
        update_time=datetime.now(),
        editor_username=editor.username,
        content=widget.content if hasattr(widget, "content") else None,
        page_id=widget.page_id,
        visible=widget.visible
    )
    db.add(widget_entity)
    db.commit()
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
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def create_widget_attachment(db: Session, widget_attachment: WidgetAttachmentCreate) -> WidgetAttachment:
    attach = WidgetAttachment(
        file_id=widget_attachment.file_id,
        widget_id=widget_attachment.widget_id,
    )
    db.add(attach)
    db.commit()
    db.refresh(attach)
    return attach


def delete_widget_attachment(db: Session, file_id: uuid.UUID) -> WidgetAttachment:
    stmt = select(WidgetAttachment).where(WidgetAttachment.file_id == file_id)
    attachment: WidgetAttachment = db.exec(stmt).first()
    if attachment:
        attachment.is_deleted = True
    db.refresh(attachment)
    return attachment


def create_doc_widget(db: Session, widget: DocWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    db.commit()
    return widget_entity


def update_doc_widget(db: Session, widget: DocWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def create_assignment_widget(db: Session, widget: AssignmentWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    assignment = AssignmentWidget(
        widget_id=widget_entity.id,
        ddl=widget.ddl,
        submit_types=[SubmitType(typ) for typ in widget.submit_types],
        max_score=widget.max_score,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    db.refresh(widget_entity)
    return widget_entity


def update_assignment_widget(db: Session, widget: AssignmentWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    widget_entity.assignment_widget.submit_types = [SubmitType[typ].value for typ in widget.submit_types]
    widget_entity.assignment_widget.ddl = widget.ddl
    widget_entity.assignment_widget.max_score = widget.max_score
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def get_assignment_widget_by_widget_id(db: Session, widget_id: int) -> AssignmentWidget:
    stmt = select(AssignmentWidget).where(AssignmentWidget.widget_id == widget_id)
    return db.exec(stmt).first()


def get_assignment_widgets_by_class_id(db: Session, class_id: int) -> list[Widget]:
    stmt = select(Widget).join(Widget.page).where(Widget.page.class_id == class_id)
    return db.exec(stmt).all()


def create_note_pdf_widget(db: Session, widget: NotePdfWidgetCreate, editor: UserInDB) -> Widget:
    widget_entity = create_widget(db, widget, editor)
    note_pdf = NotePDFWidget(
        widget_id=widget_entity.id,
        pdf_file_id=widget.pdf_file
    )
    db.add(note_pdf)
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def update_note_pdf_widget(db: Session, widget: NotePdfWidgetUpdate, editor: UserInDB) -> Widget:
    widget_entity = update_widget(db, widget, editor)
    widget_entity.note_pdf_widget.pdf_file_id = widget.pdf_file
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def delete_widget(db: Session, widget_id: int) -> Widget:
    widget_entity = get_widget(db, widget_id)
    if widget_entity:
        widget_entity.is_deleted = True
    db.commit()
    db.refresh(widget_entity)
    return widget_entity


def get_note(db: Session, note_id: int) -> Note:
    stmt = select(Note).where(Note.id == note_id).where(Note.is_deleted == False)
    note: Note = db.exec(stmt).first()
    return note


def create_note(db: Session, note: NoteCreate, editor: UserInDB) -> Note:
    widget, note_entity = get_widget(db, note.widget_id), None
    if widget:
        note_entity = Note(
            page=note.page, x=note.x, y=note.y, text=note.text,
            editor_username=editor.username,
            note_pdf_widget_id=widget.note_pdf_widget.id,
            create_time=datetime.now(),
            update_time=datetime.now()
        )
        db.add(note_entity)
        db.commit()
        db.refresh(note_entity)
    return note_entity


def update_note(db: Session, note: NoteUpdate) -> Note:
    note_entity = get_note(db, note.id)
    if note_entity:
        note_entity.page = note.page
        note_entity.x = note.x
        note_entity.y = note.y
        note_entity.text = note.text
        note_entity.update_time = datetime.now()
    db.commit()
    return note_entity


def delete_note(db: Session, note_id: int) -> Note:
    note_entity = get_note(db, note_id)
    if note_entity:
        note_entity.is_deleted = True
    db.commit()
    return note_entity
