from datetime import datetime

from pydantic import BaseModel

from backend.mjc.model.schema.common import File, Code
from backend.mjc.model.schema.user import Profile


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
    feedback: FeedBack | None = None
