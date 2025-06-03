import json
import os
import uuid
import requests

from fastapi import HTTPException, status
from sqlmodel import Session

from mjc.crud import assignment as crud_assignment, widget as crud_widget, common as crud_common
from mjc.crud.user import get_profile
from mjc.model.entity.assignment import SubmittedAssignment as SubmittedAssignmentEntity, SubmittedAssignmentFeedback
from mjc.model.entity.common import Visibility
from mjc.model.entity.widget import Widget as WidgetEntity, SubmitType
from mjc.model.schema.assignment import SubmittedAssignment, SubmittedAssignmentCreate, SubmissionAttachment, \
    FeedbackCreate, Feedback, FeedbackUpdate, FeedbackAttachment, AIFeedbackCreate, AIFeedback
from mjc.model.schema.common import Message, File, Code
from mjc.model.schema.user import UserInDB, Profile
from mjc.model.schema.widget import AssignmentWidget, TestCaseCreate, TestCaseUpdate, TestCase, TestCaseInfo, TestPoint
from mjc.service import widget as widget_service, common as common_service
from mjc import config
import mjc.utils.onlinejudge as oj


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
        submissions: list[SubmittedAssignment] = []
        return submissions


def create_submission(db: Session, submission: SubmittedAssignmentCreate, current_user: UserInDB) -> SubmittedAssignment:
    entity = crud_assignment.create_submission(db, submission, current_user.username)
    if entity:
        assignment = crud_widget.get_assignment_widget_by_widget_id(db, submission.widget_id)
        if assignment.submit_type is SubmitType.code:
            # TODO: submit to online judge
            pass
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


def get_widget_submissions_for_student(db: Session,
                                       widget_id: int,
                                       current_user: UserInDB)-> AssignmentWidget| None:
    entity = crud_widget.get_widget(db, widget_id)
    if entity:
        return get_student_submissions(db, entity, current_user.username)
    return None


def get_student_submissions(db: Session,
                            assignment_widget_entity: WidgetEntity,
                            username: str) -> AssignmentWidget | None:
    assigment_widget: AssignmentWidget = widget_service.entity2assignment(assignment_widget_entity)
    assignment_widget_id = crud_widget.get_assignment_widget_by_widget_id(db, assigment_widget.id).id
    if assigment_widget:
        submissions = crud_assignment.get_user_assignment_submissions(db, assignment_widget_id, username)
        if submissions:
            assigment_widget.status = 'submitted'
            assigment_widget.submitted_assignment =[entity2submission(db,submission) for submission in submissions]
        feedback = widget_service.get_feedback(db, assignment_widget_id, username)
        if feedback:
            assigment_widget.status = 'marked'
            assigment_widget.score = feedback.score
            assigment_widget.feedback = feedback
        return assigment_widget
    return None


def chat_with_ai(question: str, answer: str, student_answer: str) -> str:
    api_key: str = config.API_KEY
    prompt: str = config.SYSTEM_PROMPT
    content: str = f"question: {question} \nstandard_answer: {answer} \n student_answer: {student_answer}"
    url: str = config.API_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"{content}"}
        ],
        "response_format" : {
        'type': 'json_object'
        },
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


def get_ai_feedback(db: Session, request: AIFeedbackCreate) -> AIFeedback | None:
    if request.type == "text":
        feedback = json.loads(chat_with_ai(request.question, request.answer, request.student_answer))
        if feedback:
            return AIFeedback(score=feedback['score'],feedback=feedback['feedback'])
        return None
    elif request.type == "pdf":
        question = common_service.ocr4pdf(db, request.question_file_id)
        answer = common_service.ocr4pdf(db, request.answer_file_id)
        student_answer = common_service.ocr4pdf(db, request.student_answer_file_id)
        feedback = json.loads(chat_with_ai(question, answer, student_answer))
        if feedback:
            return AIFeedback(score=feedback['score'],feedback=feedback['feedback'] )
        return None
    return None


def create_test_case(db: Session, test_case: TestCaseCreate) -> TestCase:
    file_entity = crud_common.get_local_resource_file(db, test_case.file_id)
    if file_entity:
        path = file_entity.system_path
        test_case_entity = crud_assignment.create_test_case(db, test_case)
        try:
            _, info = oj.extract_test_cases(path, test_case_entity.id)
            test_case_entity.info = json.dumps(info)
            db.commit()
        except Exception as e:
            test_case_entity.assignment_widget.test_case_id = None
            db.commit()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return TestCase(
            id=test_case_entity.id,
            max_memory=test_case_entity.max_memory,
            max_cpu_time=test_case_entity.max_cpu_time,
            info=TestCaseInfo.model_validate(info)
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not found")


def update_test_case(db: Session, test_case: TestCaseUpdate) -> TestCase:
    test_case_entity = crud_assignment.get_test_case(db, test_case.id)
    info = None
    if not test_case_entity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test case not found")
    if test_case.file_id:
        file_entity = crud_common.get_local_resource_file(db, test_case.file_id)
        if not file_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not found")
        try:
            old_test_case_path = os.path.join(config.OJ_TESTCASE_URL, str(test_case.id))
            os.rename(old_test_case_path, old_test_case_path + '_old')
            _, info = oj.extract_test_cases(file_entity.path, test_case.id)
            os.removedirs(old_test_case_path + '_old')
            test_case_entity.info = json.dumps(info)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"extract test case failed, reason: {str(e)}")
    crud_assignment.update_test_case(db, test_case)
    return TestCase(
        id=test_case_entity.id,
        max_memory=test_case_entity.max_memory,
        max_cpu_time=test_case_entity.max_cpu_time,
        info=TestCaseInfo.model_validate(info) if info else None
    )


def get_widget_test_case(db: Session, widget_id: int) -> TestCase:
    test_case = crud_assignment.get_test_case(db, widget_id)
    if not test_case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")
    return TestCase(
        id=test_case.id,
        max_memory=test_case.max_memory,
        max_cpu_time=test_case.max_cpu_time,
        info=TestCaseInfo.model_validate(json.loads(test_case.info)) if test_case.info else None
    )