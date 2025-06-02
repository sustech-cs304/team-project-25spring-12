import uuid

from fastapi import APIRouter, Depends
from requests.sessions import Session

from mjc.model.schema.assignment import SubmittedAssignment, Feedback, SubmittedAssignmentCreate, \
    SubmissionAttachment, FeedbackCreate, FeedbackUpdate, FeedbackAttachment, AIFeedbackCreate
from mjc.model.schema.common import Message
from mjc.model.schema.user import UserInDB
from mjc.model.schema.widget import TestCaseCreate, TestCaseUpdate
from mjc.service.user import get_current_user
from mjc.service import assignment as assignment_service
from mjc.utils.database import SessionDep
from mjc.permission import assignment as assignment_permission
from mjc.permission import widget as widget_permission


router = APIRouter()


@router.get(path="/class/widget/{widget_id}/submission",
            response_model=list[SubmittedAssignment],
            dependencies=[Depends(assignment_permission.verify_all_submissions_get)])
async def get_all_submissions(db: SessionDep, widget_id: int) -> list[SubmittedAssignment]:
    return assignment_service.get_all_submissions(db, widget_id)


@router.post(path="/class/widget/assignment/submit",
             response_model=SubmittedAssignment,
             dependencies=[Depends(assignment_permission.verify_submission_create)])
async def create_submission(db: SessionDep,
                      submission: SubmittedAssignmentCreate,
                    current_user: UserInDB = Depends(get_current_user)) -> SubmittedAssignment:
    return assignment_service.create_submission(db, submission, current_user)


@router.post(path="/class/widget/assignment/submit/attach",
             response_model=Message,
             dependencies=[Depends(assignment_permission.verify_attach_add)])
async def add_submission_attachment(db: SessionDep, attach: SubmissionAttachment) -> Message:
    return assignment_service.add_submission_attachment(db, attach)


@router.delete(path="/class/widget/assignment/submit/attach/{file_id}",
               response_model=Message,
               dependencies=[Depends(assignment_permission.verify_attach_delete)])
async def delete_submission_attachment(db: SessionDep, file_id: uuid.UUID) -> Message:
    return assignment_service.delete_submission_attachment(db, file_id)


@router.post(path="/class/widget/assignment/feedback",
             response_model=Feedback,
             dependencies=[Depends(assignment_permission.verify_feedback_create)])
async def create_feedback(db: SessionDep,
                    feedback: FeedbackCreate,
                    current_user: UserInDB = Depends(get_current_user)) -> Feedback:
    return assignment_service.create_feedback(db, feedback, current_user)


@router.patch(path="/class/widget/assignment/feedback",
              response_model=Feedback,
              dependencies=[Depends(assignment_permission.verify_feedback_update)])
async def update_feedback(db: SessionDep,
                    feedback: FeedbackUpdate,
                    current_user: UserInDB = Depends(get_current_user)) -> Feedback:
    return assignment_service.update_feedback(db, feedback, current_user)


@router.post(path="/class/widget/assignment/feedback/attach",
             response_model=Message,
             dependencies=[Depends(assignment_permission.verify_feedback_attach_add)])
async def add_feedback_attachment(db: SessionDep,
                            attach: FeedbackAttachment) -> Message:
    return assignment_service.add_feedback_attachment(db, attach)


@router.delete(path="/class/widget/assignment/feedback/attach/{file_id}",
               response_model=Message,
               dependencies=[Depends(assignment_permission.verify_feedback_attach_delete)])
async def delete_feedback_attachment(db: SessionDep, file_id: uuid.UUID) -> Message:
    return assignment_service.delete_feedback_attachment(db, file_id)


@router.get(path="/class/widget/{widget_id}/submission/student",
            dependencies=[Depends(assignment_permission.verify_widget_get)])
async def get_widget_submissions_for_student(db: SessionDep, widget_id: int,
                                       current_user: UserInDB = Depends(get_current_user)):
    return assignment_service.get_widget_submissions_for_student(db, widget_id, current_user)


@router.post(path="/class/widget/assignment/feedback/AI")
async def get_ai_feedback(db: SessionDep, request: AIFeedbackCreate):
    return assignment_service.get_ai_feedback(db, request)


@router.get(path="/class/widget/{widget_id}/testcase",
            dependencies=[Depends(assignment_permission.verify_test_case_get)])
async def get_testcase(db: SessionDep, widget_id: int):
    return assignment_service.get_widget_test_case(db, widget_id)


@router.post(path='/class/widget/testcase',
             dependencies=[Depends(assignment_permission.verify_test_case_create)])
async def create_testcase(db: SessionDep, testcase: TestCaseCreate):
    return assignment_service.create_test_case(db, testcase)


@router.patch(path="/class/widget/testcase",
              dependencies=[Depends(assignment_permission.verify_test_case_update)])
async def update_testcase(db: SessionDep, testcase: TestCaseUpdate):
    return assignment_service.update_test_case(db, testcase)