from sqlmodel import Session, select

from backend.mjc.model.entity import SubmittedAssignment, Widget, SubmittedAssignmentFeedback


def get_submitted_assignment(db: Session, assign_id: int) -> SubmittedAssignment:
    stmt = select(SubmittedAssignment).where(SubmittedAssignment.id == assign_id)
    assign: SubmittedAssignment = db.exec(stmt).first()
    return assign


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
