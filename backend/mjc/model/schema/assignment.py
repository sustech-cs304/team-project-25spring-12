import uuid
from datetime import datetime

from pydantic import BaseModel

from mjc.model.schema.common import File, Code
from mjc.model.schema.user import Profile


class FeedbackBase(BaseModel):
    score: float | None = None
    content: str | None = None
    attachments: list[File] | None = None
    create_time: datetime | None = None
    marker: str | None = None


class Feedback(FeedbackBase):
    id: int


class FeedbackCreate(FeedbackBase):
    submission_id: int


class FeedbackUpdate(FeedbackBase):
    submission_id: int
    id: int


class SubmittedAssignmentBase(BaseModel):
    content: str | None = None
    attachments: list[File] | None = None
    code: Code | None = None


class SubmittedAssignmentCreate(SubmittedAssignmentBase):
    widget_id: int


class SubmittedAssignment(SubmittedAssignmentBase):
    id: int
    submitted_time: datetime
    student: Profile | None = None
    feedback: Feedback | None = None


class SubmissionAttachment(BaseModel):
    submission_id: int
    file_id: uuid.UUID


class FeedbackAttachment(BaseModel):
    feedback_id: int
    file_id: uuid.UUID


class DDL(BaseModel):
    class_id: int
    class_name: str
    widget_id: int
    widget_title: str
    page_id: int
    page_name: str
    ddl: datetime
    course_code: str


class AIFeedbackCreate(BaseModel):
    type: str | None = "text"
    question: str | None = None
    answer: str | None = None
    student_answer: str | None = None
    question_file_id: uuid.UUID | None = None
    answer_file_id: uuid.UUID | None = None
    student_answer_file_id: uuid.UUID | None = None


class AIFeedback(BaseModel):
    score: float | None = None
    feedback: str
