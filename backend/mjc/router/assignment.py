import uuid

from fastapi import APIRouter, Depends

from mjc.model.schema.assignment import SubmittedAssignment, Feedback, SubmittedAssignmentCreate, \
    SubmissionAttachment, FeedbackCreate, FeedbackUpdate, FeedbackAttachment
from mjc.model.schema.common import Message
from mjc.model.schema.user import UserInDB
from mjc.service.user import get_current_user
from mjc.service import assignment as assignment_service
from mjc.utils.database import SessionDep


router = APIRouter()


@router.get(path="/class/widget/{widget_id}/submission", response_model=list[SubmittedAssignment])
def get_all_submissions(db: SessionDep, widget_id: int) -> list[SubmittedAssignment]:
    return assignment_service.get_all_submissions(db, widget_id)


@router.post(path="/class/widget/assignment/submit", response_model=SubmittedAssignment)
def create_submission(db: SessionDep,
                      submission: SubmittedAssignmentCreate,
                    current_user: UserInDB = Depends(get_current_user)) -> SubmittedAssignment:
    return assignment_service.create_submission(db, submission, current_user)


@router.post(path="/class/widget/assignment/submit/attach", response_model=Message)
def add_submission_attachment(db: SessionDep, attach: SubmissionAttachment) -> Message:
    return assignment_service.add_submission_attachment(db, attach)


@router.delete(path="/class/widget/assignment/submit/attach/{file_id}", response_model=Message)
def delete_submission_attachment(db: SessionDep, file_id: uuid.UUID) -> Message:
    return assignment_service.delete_submission_attachment(db, file_id)


@router.post(path="/class/widget/assignment/feedback", response_model=Feedback)
def create_feedback(db: SessionDep,
                    feedback: FeedbackCreate,
                    current_user: UserInDB = Depends(get_current_user)) -> Feedback:
    return assignment_service.create_feedback(db, feedback, current_user)


@router.patch(path="/class/widget/assignment/feedback", response_model=Feedback)
def update_feedback(db: SessionDep,
                    feedback: FeedbackUpdate,
                    current_user: UserInDB = Depends(get_current_user)) -> Feedback:
    return assignment_service.update_feedback(db, feedback, current_user)


@router.post(path="/class/widget/assignment/feedback/attach", response_model=Message)
def add_feedback_attachment(db: SessionDep,
                            attach: FeedbackAttachment) -> Message:
    return assignment_service.add_feedback_attachment(db, attach)


@router.delete(path="/class/widget/assignment/feedback/attach/{file_id}", response_model=Message)
def delete_feedback_attachment(db: SessionDep, file_id: uuid.UUID) -> Message:
    return assignment_service.delete_feedback_attachment(db, file_id)
