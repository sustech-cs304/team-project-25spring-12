import uuid
from datetime import datetime

from sqlmodel import Session, select

from backend.mjc.model.schema.assignment import SubmittedAssignmentCreate, FeedbackCreate, FeedbackUpdate
from backend.mjc.model.schema.assignment import SubmissionAttachment , FeedbackAttachment
from backend.mjc.model.entity import SubmittedAssignment, Widget, SubmittedAssignmentFeedback
from backend.mjc.model.entity import SubmittedAssignmentAttachment, FeedbackAttachment as FeedbackAttachmentEntity


def get_all_assignments_submissions(db: Session, widget_id: int) -> list[SubmittedAssignment]:
    stmt = select(SubmittedAssignment).where(SubmittedAssignment.widget_id == widget_id).join(Widget).where(Widget.is_deleted == False)
    submissions: list[SubmittedAssignment] = db.exec(stmt).all()
    return submissions


def get_user_assignment_submissions(db: Session, widget_id: int, username: str) -> list[SubmittedAssignment]:
    stmt = select(SubmittedAssignment) \
                .where(SubmittedAssignment.widget_id == widget_id) \
                .where(SubmittedAssignment.username == username) \
                .join(Widget) \
                .where(Widget.is_deleted == False)
    submissions: list[SubmittedAssignment] = db.exec(stmt).all()
    return submissions


def get_last_feedback(db: Session, widget_id: int, username: str) -> SubmittedAssignmentFeedback:
    stmt = select(SubmittedAssignment) \
            .where(SubmittedAssignment.widget_id == widget_id) \
            .where(SubmittedAssignment.username == username) \
            .order_by(SubmittedAssignment.feedback.create_time.desc()).limit(1)
    feedback = db.exec(stmt).first().feedback
    return feedback


def create_submission(db: Session, submission: SubmittedAssignmentCreate, username: str) -> SubmittedAssignment:
    submission_entity = SubmittedAssignment(
        create_time=datetime.now(),
        assignment_widget_id=submission.widget_id,
        username=username,
        content=submission.content,
        code=submission.code.content,
        language=submission.code.language
    )
    db.add(submission_entity)
    db.commit()
    db.refresh(submission_entity)
    return submission_entity


def create_feedback(db: Session, feedback: FeedbackCreate, username: str) -> SubmittedAssignmentFeedback:
    feedback_entity = SubmittedAssignmentFeedback(
        score=feedback.score,
        content=feedback.content,
        create_time=datetime.now(),
        submitted_assignment_id=feedback.submission_id,
        maker=username
    )
    db.add(feedback_entity)
    db.commit()
    db.refresh(feedback_entity)
    return feedback_entity


def update_feedback(db: Session, feedback: FeedbackUpdate, username: str) -> SubmittedAssignmentFeedback:
    stmt = select(SubmittedAssignmentFeedback).where(SubmittedAssignmentFeedback.id == feedback.id)
    feedback_entity: SubmittedAssignmentFeedback = db.exec(stmt).first()
    feedback_entity.score = feedback.score
    feedback_entity.content = feedback.content
    feedback_entity.marker = username
    feedback_entity.create_time = datetime.now()
    db.commit()
    db.refresh(feedback_entity)
    return feedback_entity


def create_submission_attachment(db: Session, submission_attachment: SubmissionAttachment) -> SubmittedAssignmentAttachment:
    attach = SubmittedAssignmentAttachment(
        file_id=submission_attachment.file.id,
        subitted_assignment_id = submission_attachment.submission_id,
    )
    db.add(attach)
    db.commit()
    db.refresh(attach)
    return attach


def delete_submission_attachment(db: Session, file_id: uuid.UUID) -> SubmittedAssignmentAttachment:
    stmt = select(SubmittedAssignmentAttachment) \
                .where(SubmittedAssignmentAttachment.file_id == file_id)
    attachment: SubmittedAssignmentAttachment = db.exec(stmt).first()
    if attachment:
        attachment.is_deleted = True
    db.commit()
    db.refresh(attachment)
    return attachment


def create_feedback_attachment(db: Session, feedback_attachment: FeedbackAttachment) -> FeedbackAttachmentEntity:
    attach = FeedbackAttachmentEntity(
        file_id=feedback_attachment.file.id,
        feedback_id=feedback_attachment.id,
    )
    db.add(attach)
    db.commit()
    db.refresh(attach)
    return attach


def delete_feedback_attachment(db: Session, file_id: uuid.UUID) -> FeedbackAttachmentEntity:
    stmt = select(FeedbackAttachmentEntity) .where(FeedbackAttachmentEntity.file_id == file_id)
    attachment: FeedbackAttachmentEntity = db.exec(stmt).first()
    if attachment:
        attachment.is_deleted = True
    db.commit()
    db.refresh(attachment)
    return attachment
