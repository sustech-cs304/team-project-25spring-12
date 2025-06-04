import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from mjc.model.schema.common import File
from mjc.model.schema.widget import AssignmentWidget
from mjc.model.schema.user import Profile
from mjc.model.entity.argue import ArguePostStatus


class ArguePostCommentBase(BaseModel):
    content: str
    reply_to: int | None = None


class ArguePostComment(ArguePostCommentBase):
    id: int
    editor: Profile
    create_time: datetime


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


class ArguePost(ArguePostBase):
    id: int
    create_time: datetime
    update_time: datetime
    watch: int
    is_watched : bool | None = False
    is_voted: bool | None = False
    support: int
    editor: Profile
    not_support: int
    attachments: list[File] | None = None
    comments: list[ArguePostComment] | None = Field(default_factory=[])
    feedback: ArguePostFeedback | None = None
    old_score: float
    assignment: AssignmentWidget
    status: ArguePostStatus = ArguePostStatus.SUBMITTED


class ArguePostCard(ArguePostBase):
    id: int
    create_time: datetime
    update_time: datetime
    watch: int | None = 0
    is_watched: bool | None = False
    is_voted: bool | None = False
    support: int | None = 0
    not_support: int | None = 0
    editor: Profile
    comments: int | None = 0
    status: ArguePostStatus = ArguePostStatus.SUBMITTED


class ArguePostCreate(ArguePostBase):
    submitted_assignment_id: int


class ArguePostUpdate(BaseModel):
    id: int
    title: str
    content: str


class ArguePostAttachmentCreate(BaseModel):
    argue_post_id: int
    file_id: uuid.UUID


class ArguePostFeedbackAttachmentCreate(BaseModel):
    argue_post_feedback_id: int
    file_id: uuid.UUID


class ArguePostWatchCreate(BaseModel):
    argue_post_id: int