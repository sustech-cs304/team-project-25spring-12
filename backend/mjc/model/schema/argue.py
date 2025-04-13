import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from backend.mjc.model.schema.common import File
from backend.mjc.model.schema.widget import AssignmentWidget
from backend.mjc.model.schema.user import Profile


class ArguePostCommentBase(BaseModel):
    content: str
    reply_to: int | None = None


class ArguePostComment(ArguePostCommentBase):
    id: int
    editor: Profile


class ArguePostCommentCreate(ArguePostCommentBase):
    argue_post_id: int


class ArguePostVoteCreate(BaseModel):
    argue_post_id: int
    is_support: bool


class ArguePostFeedbackBase(BaseModel):
    argue_post_id: int
    content: str | None
    score: float


class ArguePostFeedback(ArguePostFeedbackBase):
    id: int
    marker: Profile
    attachments: list[File] | None = None


class ArguePostFeedbackCreate(ArguePostFeedbackBase):
    pass


class ArguePostBase(BaseModel):
    widget_id: int
    submitted_assignment_id: int | None = None
    title: str
    content: str | None = None


class ArguePost(BaseModel):
    id: int
    assignment: AssignmentWidget
    create_time: datetime
    update_time: datetime
    watch: int
    support: int
    editor: Profile
    not_support: int
    attachments: list[File] | None = None
    comments: list[ArguePostComment] | None = Field(default_factory=[])
    feedback: ArguePostFeedback | None = None


class ArguePostCard(ArguePostBase):
    create_time: datetime
    update_time: datetime
    watch: int | None = 0
    support: int | None = 0
    not_support: int | None = 0
    editor: Profile
    comments: int | None = 0


class ArguePostCreate(ArguePostBase):
    submitted_assignment_id: int


class ArguePostUpdate(ArguePostBase):
    id: int


class ArguePostAttachmentCreate(BaseModel):
    argue_post_id: int
    file_id: uuid.UUID


class ArguePostFeedbackAttachmentCreate(BaseModel):
    argue_post_feedback_id: int
    file_id: uuid.UUID