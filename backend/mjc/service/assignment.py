import uuid

from fastapi import HTTPException, status
from sqlmodel import Session

from mjc.crud import assignment as crud_assignment
from mjc.crud.user import get_profile

from mjc.model.entity.assignment import SubmittedAssignment as SubmittedAssignmentEntity, SubmittedAssignmentFeedback
from mjc.model.entity.common import Visibility
from mjc.model.schema.assignment import SubmittedAssignment, SubmittedAssignmentCreate, SubmissionAttachment, \
    FeedbackCreate, Feedback, FeedbackUpdate, FeedbackAttachment
from mjc.model.schema.common import Message, File, Code
from mjc.model.schema.user import UserInDB, Profile


def entity2submission(db: Session, entity: SubmittedAssignmentEntity) -> SubmittedAssignment:
    submission = SubmittedAssignment(
        id=entity.id,
        content=entity.content,
        code= Code(code=entity.code,
                   language=entity.language) if entity.code else None,
        submitted_time=entity.create_time,
        student=Profile.model_validate(get_profile(db, entity.username).model_dump()),
        attachments=[File(url=None,
                          id=file.file_id,
                          filename=file.file.filename,
                          visibility=Visibility.public) for file in entity.attachments if entity.attachments],
    )
    return submission


def entity2feedback(entity: SubmittedAssignmentFeedback) -> Feedback:
    feedback = Feedback(
        id=entity.id,
        score=entity.score,
        content=entity.content,
        attachments=[File(url=None,
                          id=file.file_id,
                          filename=file.file.filename,
                          visibility=Visibility.public) for file in entity.attachments if entity.attachments],
        create_time=entity.create_time,
        marker=entity.marker
    )
    return feedback


def get_all_submissions(db: Session, assignment_widget_id: int) -> list[SubmittedAssignment] | None:
    entities = crud_assignment.get_all_assignments_submissions(db, assignment_widget_id)
    if entities:
        submissions: list[SubmittedAssignment] = [entity2submission(db, entity) for entity in entities]
        return submissions
    else:
        return None


def create_submission(db: Session, submission: SubmittedAssignmentCreate, current_user: UserInDB) -> SubmittedAssignment:
    entity = crud_assignment.create_submission(db, submission, current_user.username)
    if entity:
        return entity2submission(db, entity)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create submission failed")


def add_submission_attachment(db: Session, attach: SubmissionAttachment) -> Message:
    entity = crud_assignment.create_submission_attachment(db, attach)
    if entity:
        return Message(msg="add success")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Add submission attachment failed")


def delete_submission_attachment(db: Session, file_id: uuid.UUID) -> Message:
    entity = crud_assignment.delete_submission_attachment(db, file_id)
    if entity:
        return Message(msg="delete success")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete submission attachment failed")


def create_feedback(db: Session, feedback: FeedbackCreate, current_user: UserInDB) -> Feedback:
    entity = crud_assignment.create_feedback(db, feedback, current_user.username)
    if entity:
        return entity2feedback(entity)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create feedback failed")


def update_feedback(db: Session, feedback: FeedbackUpdate, current_user: UserInDB) -> Feedback:
    entity = crud_assignment.update_feedback(db, feedback, current_user.username)
    if entity:
        return entity2feedback(entity)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update feedback failed")


def add_feedback_attachment(db: Session, attach: FeedbackAttachment) -> Message:
    entity = crud_assignment.create_feedback_attachment(db, attach)
    if entity:
        return Message(msg="add success")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Add feedback attachment failed")


def delete_feedback_attachment(db: Session, file_id: uuid.UUID) -> Message:
    entity = crud_assignment.delete_feedback_attachment(db, file_id)
    if entity:
        return Message(msg="delete success")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete feedback attachment failed")
