import uuid

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.model.entity.assignment import SubmittedAssignment, FeedbackAttachment
from mjc.model.schema.assignment import SubmittedAssignmentCreate, SubmissionAttachment, FeedbackCreate, FeedbackUpdate
from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.service.user import get_current_user
from mjc.crud import widget as crud_widget, assignment as crud_assignment
from mjc.permission.common import verify_class_admin, verify_user_in_class


def verify_submission_exists(db: Session, submission_id: int) -> SubmittedAssignment:
    submission = crud_assignment.get_submitted_assignment(db, submission_id)
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission


async def verify_all_submissions_get(db: SessionDep, widget_id: int,
                                     current_user: UserInDB = Depends(get_current_user)):
    widget = crud_widget.get_widget(db, widget_id)
    if widget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    verify_class_admin(db, widget.page.class_id, current_user)


async def verify_widget_get(db: SessionDep, widget_id: int,
                            current_user: UserInDB = Depends(get_current_user)):
    widget = crud_widget.get_widget(db, widget_id)
    if widget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    verify_user_in_class(db, widget.class_id, current_user)


async def verify_submission_create(db: SessionDep, submission: SubmittedAssignmentCreate,
                                   current_user: UserInDB = Depends(get_current_user)):
    widget = crud_widget.get_widget(db, submission.widget_id)
    if widget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    verify_user_in_class(db, widget.page.class_id, current_user)


async def verify_attach_add(db: SessionDep, attach: SubmissionAttachment,
                            current_user: UserInDB = Depends(get_current_user)):
    submission = verify_submission_exists(db, attach.submission_id)
    if submission.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to do this")
    verify_user_in_class(db, submission.assignment_widget.widget.page.class_id, current_user)


async def verify_attach_delete(db: SessionDep, file_id: uuid.UUID,
                               current_user: UserInDB = Depends(get_current_user)):
    attach = crud_assignment.get_submission_attach(db, file_id)
    if attach is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    if attach.submitted_assignment.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to do this")


async def verify_feedback_create(db: SessionDep, feedback: FeedbackCreate,
                                 current_user: UserInDB = Depends(get_current_user)):
    submission = verify_submission_exists(db, feedback.submission_id)
    verify_class_admin(db, submission.assignment_widget.widget.page.class_id, current_user)


async def verify_feedback_update(db: SessionDep, feedback: FeedbackUpdate,
                                 current_user: UserInDB = Depends(get_current_user)):
    submission = verify_submission_exists(db, feedback.submission_id)
    verify_class_admin(db, submission.assignment_widget.widget.page.class_id, current_user)


async def verify_feedback_attach_add(db: SessionDep, attach: FeedbackAttachment,
                                     current_user: UserInDB = Depends(get_current_user)):
    feedback = crud_assignment.get_feedback(db, attach.feedback_id)
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    submission = verify_submission_exists(db, feedback.submission_id)
    verify_class_admin(db, submission.assignment_widget.widget.page.class_id, current_user)


async def verify_feedback_attach_delete(db: SessionDep, file_id: uuid.UUID,
                                        current_user: UserInDB = Depends(get_current_user)):
    attach = crud_assignment.get_feedback_attach(db, file_id)
    if attach is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    if attach.submitted_assignment.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to do this")
