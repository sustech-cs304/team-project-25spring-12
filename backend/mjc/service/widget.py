from fastapi import HTTPException, status
from sqlmodel import Session

import backend.mjc.crud.assignment
from backend.mjc.crud import widget as crud_widget
from backend.mjc.model.schema.user import UserInDB, Profile
from backend.mjc.model.schema.widget import AssignmentWidget, NotePdfWidget, DocWidget, DocWidgetCreate, \
    DocWidgetUpdate, Note, NoteCreate, NoteUpdate, \
    AssignmentWidgetCreate, AssignmentWidgetUpdate, NotePdfWidgetCreate, NotePdfWidgetUpdate, WidgetAttachmentCreate
from backend.mjc.model.schema.assignment import Feedback, SubmittedAssignment
from backend.mjc.model.schema.common import File, Message
from backend.mjc.model.entity import Widget as WidgetEntity, WidgetType
from backend.mjc.model.entity import SubmittedAssignment as SubmittedAssignmentEntity
from backend.mjc.model.entity import SubmittedAssignmentFeedback as FeedbackEntity


def entity2doc(entity: WidgetEntity) -> DocWidget:
    attach: list[File] = []
    if entity.attachments:
        for attachment in entity.attachment:
            file: File = File(id=attachment.file_id,
                              filename=attachment.name,
                              visibility=attachment.file.visibility,
                              url=None)
            attach.append(file)
    doc_widget = DocWidget(
        title=entity.title,
        index=entity.index,
        type=entity.type,
        create_time=entity.create_time,
        update_time=entity.update_time,
        editor=Profile.model_validate(entity.editor.model_dump()),
        visible=entity.visible,
        id=entity.id,
        content=entity.content if entity.content else None,
        attachments=attach
    )
    return doc_widget


def entity2submission(entity: SubmittedAssignmentEntity) -> SubmittedAssignment:
    submission = SubmittedAssignment(
        id=entity.id,
        content=entity.content,
        code= entity.code,
        submitted_time=entity.submitted_time,
        student=None,
        attachments=[File(url=None, **file.model_dump()) for file in entity.attachments if entity.attachments],
    )
    return submission


def get_feedback(db: Session, widget_id: int, username: str) -> Feedback | None:
    entity: FeedbackEntity = backend.mjc.crud.assignment.get_last_feedback(db, widget_id, username)
    if entity:
        feedback = Feedback(score=entity.score,
                            content=entity.content,
                            attachments=[File(url=None, **file.model_dump()) for file in entity.attachments if entity.attachments],
                            create_time=entity.create_time,
                            id=entity.id)
        return feedback
    return None


def entity2assignment(entity: WidgetEntity) -> AssignmentWidget:
    assignment_widget = AssignmentWidget(
        title=entity.title,
        index=entity.index,
        type=entity.type,
        create_time=entity.create_time,
        update_time=entity.update_time,
        editor=Profile.model_validate(entity.editor.model_dump()),
        visible=entity.visible,
        id=entity.id,
        content=entity.content if entity.content else None,
        submit_types=entity.assignment_widget.submit_types,
        submitted_assignment=None,
        status='not submitted',
        ddl=entity.assignment_widget.ddl,
        score=None,
        max_score=entity.assignment_widget.max_score,
        feedback=None,
        attachments=[File(url=None, **file.model_dump()) for file in entity.attachments if entity.attachments]
    )
    return assignment_widget


def entity2notepdf(entity: WidgetEntity) -> NotePdfWidget:
    note_pdf_widget = NotePdfWidget(
        title=entity.title,
        index=entity.index,
        type=entity.type,
        create_time=entity.create_time,
        update_time=entity.update_time,
        editor=Profile.model_validate(entity.editor.model_dump()),
        visible=entity.visible,
        id=entity.id,
        pdf_file=File(
            id=entity.note_pdf_widget.pdf_file.id,
            filename=entity.note_pdf_widget.pdf_file.filename,
            visibility=entity.note_pdf_widget.pdf_file.visibility,
            url=None
        ),
    )
    return note_pdf_widget


def entity2widget(entity: WidgetEntity) -> AssignmentWidget | NotePdfWidget | DocWidget | None:
    if entity.type == WidgetType.doc:
        return entity2doc(entity)
    elif entity.type == WidgetType.assignment:
        return entity2assignment(entity)
    elif entity.type == WidgetType.note_pdf:
        return entity2notepdf(entity)


def get_student_submissions(db: Session,
                            assignment_widget_entity: WidgetEntity,
                            username: str):
    assigment_widget: AssignmentWidget = entity2assignment(assignment_widget_entity)
    if assigment_widget:
        submissions = backend.mjc.crud.assignment.get_user_assignment_submissions(db, assigment_widget.id, username)
        if submissions:
            assigment_widget.status = 'submitted'
            assigment_widget.submitted_assignment =[entity2submission(submission) for submission in submissions]
        feedback = get_feedback(db, assignment_widget_entity.id, username)
        if feedback:
            assigment_widget.status = 'marked'
            assigment_widget.score = feedback.score
            assigment_widget.feedback = feedback
        return assigment_widget
    return None


def get_all_student_submissions(db: Session, widget_id: int) -> list[SubmittedAssignment] | None:
    entities: list[SubmittedAssignmentEntity] = backend.mjc.crud.assignment.get_all_assignments_submissions(db, widget_id)
    submissions: list[SubmittedAssignment] =[]
    if entities:
        for entity in entities:
            submission = entity2submission(entity)
            submission.feedback = Feedback(score=entity.feedback.score,
                                           content=entity.feedback.content,
                                           attachments=[File(url=None, **file.model_dump()) \
                                                        for file in entity.feedback.attachments if entity.feedback.attachments],
                                           create_time=entity.create_time,
                                           id=entity.feedback.id) if entity.feedback else None
            submissions.append(submission)
        return submissions
    return None


def create_doc_widget(db: Session, editor: UserInDB, doc_widget_create: DocWidgetCreate) -> DocWidget:
    if doc_widget_create.type == WidgetType.doc:
        widget_entity = crud_widget.create_doc_widget(db, doc_widget_create, editor)
        if widget_entity:
            doc_widget = entity2widget(widget_entity)
            return doc_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create doc widget failed")


def update_doc_widget(db:Session, editor: UserInDB, doc_widget_update: DocWidgetUpdate) -> DocWidget:
    if doc_widget_update.type == WidgetType.doc:
        widget_entity = crud_widget.update_doc_widget(db, doc_widget_update, editor)
        if widget_entity:
            doc_widget = entity2widget(widget_entity)
            return doc_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update doc widget failed")


def create_assignment_widget(db:Session, editor:UserInDB, assignment_widget_create: AssignmentWidgetCreate) -> AssignmentWidget:
    if assignment_widget_create.type == WidgetType.assignment:
        widget_entity = crud_widget.create_assignment_widget(db, assignment_widget_create, editor)
        if widget_entity:
            assignment_widget = entity2widget(widget_entity)
            return assignment_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create assignment widget failed")


def update_assignment_widget(db:Session, editor: UserInDB, assignment_widget_update: AssignmentWidgetUpdate) -> AssignmentWidget:
    if assignment_widget_update.type == WidgetType.assignment:
        widget_entity = crud_widget.update_assignment_widget(db, assignment_widget_update, editor)
        if widget_entity:
            assignment_widget = entity2widget(widget_entity)
            return assignment_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update assignment widget failed")


def create_note_pdf_widget(db:Session, editor:UserInDB, note_pdf_widget_create: NotePdfWidgetCreate) -> NotePdfWidget:
    if note_pdf_widget_create.type == WidgetType.note_pdf:
        widget_entity = crud_widget.create_note_pdf_widget(db, note_pdf_widget_create, editor)
        if widget_entity:
            note_pdf_widget = entity2widget(widget_entity)
            return note_pdf_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create note pdf widget failed")


def update_note_pdf_widget(db: Session, editor:UserInDB, note_pdf_widget_update: NotePdfWidgetUpdate) -> NotePdfWidget:
    if note_pdf_widget_update.type == WidgetType.note_pdf:
        widget_entity = crud_widget.update_widget(db, note_pdf_widget_update,editor)
        if widget_entity:
            note_pdf_widget = entity2widget(widget_entity)
            return note_pdf_widget
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update note pdf widget failed")


def delete_widget(db: Session, widget_id: int) -> Message:
    widget_entity = crud_widget.delete_widget(db, widget_id)
    if widget_entity:
        return Message(msg="Widget deleted successfully")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete widget failed")


def add_widget_attachment(db: Session, attachment: WidgetAttachmentCreate) -> DocWidget | AssignmentWidget | NotePdfWidget:

    pass


def delete_attachment(db: Session, attachment_id: int):
    attachment_entity = crud_widget.delete_widget(db, attachment_id)
    if attachment_entity:
        return attachment_entity
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete attachment failed")


def create_note(db: Session, note: NoteCreate, editor: UserInDB) -> Note:
    note_entity = crud_widget.create_note(db, note, editor)
    return Note.model_validate(note_entity.model_dump())


def update_note(db: Session, note: NoteUpdate, editor: UserInDB) -> Note:
    note_entity = crud_widget.update_note(db, note)
    return Note.model_validate(note_entity.model_dump())


def delete_note(db: Session, note_id: int, editor: UserInDB) -> Message:
    crud_widget.delete_note(db, note_id)
    return Message(msg='Success')