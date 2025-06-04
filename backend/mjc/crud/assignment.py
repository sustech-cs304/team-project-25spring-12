import uuid
from datetime import datetime

from sqlmodel import Session, select, desc

from mjc.crud.widget import get_widget
from mjc.model.schema.widget import TestCaseCreate, TestCaseUpdate
from mjc.model.schema.assignment import SubmittedAssignmentCreate, FeedbackCreate, FeedbackUpdate
from mjc.model.schema.assignment import SubmissionAttachment, FeedbackAttachment
from mjc.model.entity.widget import Widget, AssignmentWidget, TestCase
from mjc.model.entity.assignment import SubmittedAssignment, SubmittedAssignmentFeedback, \
    SubmittedAssignmentAttachment, FeedbackAttachment as FeedbackAttachmentEntity


def get_submitted_assignment(db: Session, assign_id: int) -> SubmittedAssignment:
    stmt = select(SubmittedAssignment).where(SubmittedAssignment.id == assign_id)
    assign: SubmittedAssignment = db.exec(stmt).first()
    return assign


def get_all_assignments_submissions(db: Session, widget_id: int) -> list[SubmittedAssignment]:
    widget = get_widget(db, widget_id)
    stmt = select(SubmittedAssignment).where(SubmittedAssignment.assignment_widget_id == widget.assignment_widget.id). \
        join(SubmittedAssignment.assignment_widget).join(AssignmentWidget.widget).where(Widget.is_deleted == False)
    submissions: list[SubmittedAssignment] = db.exec(stmt).all()
    return submissions


def get_user_assignment_submissions(db: Session, assignment_widget_id: int, username: str) -> list[SubmittedAssignment]:
    stmt = select(SubmittedAssignment) \
                .where(SubmittedAssignment.assignment_widget_id == assignment_widget_id) \
                .where(SubmittedAssignment.username == username) \
                .join(SubmittedAssignment.assignment_widget).join(AssignmentWidget.widget).where(Widget.is_deleted == False)
    submissions: list[SubmittedAssignment] = db.exec(stmt).all()
    return submissions


def get_feedback(db: Session, feedback_id: int) -> SubmittedAssignmentFeedback:
    stmt = select(SubmittedAssignmentFeedback).where(SubmittedAssignmentFeedback.id == feedback_id)
    feedback = db.exec(stmt).first()
    return feedback


def get_last_feedback(db: Session, widget_id: int, username: str) -> SubmittedAssignmentFeedback | None:
    stmt = select(SubmittedAssignment) \
            .where(SubmittedAssignment.assignment_widget_id == widget_id) \
            .where(SubmittedAssignment.username == username) \
            .join(SubmittedAssignment.feedback) \
            .order_by(desc(SubmittedAssignmentFeedback.create_time)).limit(1)
    submitted = db.exec(stmt).first()
    if submitted:
        return submitted.feedback
    return None


def get_submission_attach(db: Session, file_id: uuid.UUID) -> SubmittedAssignmentAttachment:
    stmt = select(SubmittedAssignmentAttachment) \
            .where(SubmittedAssignmentAttachment.file_id == file_id) \
            .where(SubmittedAssignmentAttachment.is_deleted == False)

    attachment: SubmittedAssignmentAttachment = db.exec(stmt).first()
    return attachment


def get_feedback_attach(db: Session, file_id: uuid.UUID) -> FeedbackAttachmentEntity:
    stmt = select(FeedbackAttachmentEntity) \
            .where(FeedbackAttachmentEntity.file_id == file_id) \
            .where(FeedbackAttachmentEntity.is_deleted == False)
    attachment: FeedbackAttachment = db.exec(stmt).first()
    return attachment


def create_submission(db: Session, submission: SubmittedAssignmentCreate, username: str) -> SubmittedAssignment | None:
    widget = get_widget(db, submission.widget_id)
    if widget:
        submission_entity = SubmittedAssignment(
            create_time=datetime.now(),
            assignment_widget_id=widget.assignment_widget.id,
            username=username,
            content=submission.content,
            code=submission.code.code if submission.code else None,
            language=submission.code.language if submission.code else None,
        )
        db.add(submission_entity)
        db.commit()
        db.refresh(submission_entity)
        return submission_entity
    return None


def create_feedback(db: Session, feedback: FeedbackCreate, username: str) -> SubmittedAssignmentFeedback:
    feedback_entity = SubmittedAssignmentFeedback(
        score=feedback.score,
        content=feedback.content,
        create_time=datetime.now(),
        submitted_assignment_id=feedback.submission_id,
        marker=username
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
        file_id=submission_attachment.file_id,
        submitted_assignment_id = submission_attachment.submission_id,
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
        file_id=feedback_attachment.file_id,
        feedback_id=feedback_attachment.feedback_id,
    )
    db.add(attach)
    db.commit()
    db.refresh(attach)
    return attach


def delete_feedback_attachment(db: Session, file_id: uuid.UUID) -> FeedbackAttachmentEntity:
    stmt = select(FeedbackAttachmentEntity).where(FeedbackAttachmentEntity.file_id == file_id)
    attachment: FeedbackAttachmentEntity = db.exec(stmt).first()
    if attachment:
        attachment.is_deleted = True
    db.commit()
    db.refresh(attachment)
    return attachment


def get_widget_test_case(db: Session, widget_id: int) -> TestCase:
    stmt = select(TestCase).join(TestCase.assignment_widget) \
                           .join(AssignmentWidget.widget) \
                           .where(Widget.id == widget_id)
    test_case = db.exec(stmt).first()
    return test_case


def get_test_case(db: Session, test_case_id: int) -> TestCase:
    stmt = select(TestCase).where(TestCase.id == test_case_id)
    return db.exec(stmt).first()


def create_test_case(db: Session, test_case: TestCaseCreate) -> TestCase | None:
    assignment_widget = get_widget(db, test_case.widget_id).assignment_widget
    if assignment_widget:
        entity = TestCase(
            max_cpu_times=test_case.max_cpu_time,
            max_memory=test_case.max_memory
        )
        db.add(entity)
        db.commit()
        assignment_widget.test_case_id = entity.id
        db.commit()
        db.refresh(entity)
        return entity
    return None


def update_test_case(db: Session, test_case: TestCaseUpdate) -> TestCase:
    stmt = select(TestCase).where(TestCase.id == test_case.id)
    entity: TestCase = db.exec(stmt).first()
    if entity:
        entity.max_cpu_time = test_case.max_cpu_time
        entity.max_memory = test_case.max_memory
        db.commit()
    return entity