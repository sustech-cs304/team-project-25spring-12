import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.assignment import SubmittedAssignment
    from mjc.model.entity.common import LocalResourceFile
    from mjc.model.entity.widget import Widget
    from mjc.model.entity.user import Profile


class ArguePostStatus(str, Enum):
    SUBMITTED = "submitted"
    PROCESSED = "processed"
    CLOSED = "closed"


class ArguePost(SQLModel, table=True):
    __tablename__ = 'argue_post'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    submitted_assignment_id: int = Field(foreign_key="submitted_assignment.id")
    title: str | None = Field(default=None, nullable=True)
    create_time: datetime | None = Field(default=None, nullable=True)
    update_time: datetime | None = Field(default=None, nullable=True)
    content: str | None = Field(default=None, nullable=True)
    status: ArguePostStatus = Field(default=ArguePostStatus.SUBMITTED, sa_column=Column(SQLEnum(ArguePostStatus)))
    watch: int | None = 0
    is_deleted: bool = Field(default=False, nullable=False)
    old_score: float = Field(default=0.0, nullable=False)
    editor_username: str | None = Field(foreign_key="profile.username")

    widget: "Widget" = Relationship()
    feedback: "ArguePostFeedback" = Relationship(back_populates="argue_post")
    editor: "Profile" = Relationship()
    attachments: list["ArguePostAttachment"] = Relationship(back_populates="argue_post")
    comments: list["ArguePostComment"] = Relationship(back_populates="argue_post")
    submitted_assignment: "SubmittedAssignment" = Relationship(back_populates="argue_post")


class ArguePostAttachment(SQLModel, table=True):
    __tablename__ = 'argue_post_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    argue_post_id: int = Field(foreign_key="argue_post.id")
    is_deleted: bool = Field(default=False, nullable=False)

    file: "LocalResourceFile" = Relationship()
    argue_post: "ArguePost" = Relationship(back_populates="attachments")


class ArguePostComment(SQLModel, table=True):
    __tablename__ = 'argue_post_comment'

    id: int | None = Field(default=None, primary_key=True)
    argue_post_id: int = Field(foreign_key="argue_post.id")
    reply_to: int | None = Field(default=None, nullable=True, foreign_key="argue_post_comment.id")
    editor_username: str = Field(foreign_key="profile.username")
    content: str | None = Field(default=None, nullable=True)
    create_time: datetime | None = Field(default=None, nullable=True)

    argue_post: "ArguePost" = Relationship(back_populates="comments")
    reply_to_comment: "ArguePostComment" = Relationship()
    editor: "Profile" = Relationship()


class ArguePostVote(SQLModel, table=True):
    __tablename__ = 'argue_post_vote'

    id: int | None = Field(default=None, primary_key=True)
    argue_post_id: int = Field(foreign_key="argue_post.id")
    is_support: bool
    voter_username: str = Field(foreign_key="profile.username")

    argue_post: "ArguePost" = Relationship()
    voter: "Profile" = Relationship()


class ArguePostWatch(SQLModel, table=True):
    __tablename__ = 'argue_post_watch'

    id: int | None = Field(default=None, primary_key=True)
    argue_post_id: int = Field(foreign_key="argue_post.id")
    watcher_username: str = Field(foreign_key="profile.username")
    is_deleted: bool = Field(default=False)

    argue_post: "ArguePost" = Relationship()
    watcher: "Profile" = Relationship()


class ArguePostFeedbackAttachment(SQLModel, table=True):
    __tablename__ = 'argue_post_feedback_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    argue_post_feedback_id: int = Field(foreign_key="argue_post_feedback.id")
    is_deleted: bool = Field(default=False)

    file: "LocalResourceFile" = Relationship()
    argue_post_feedback: "ArguePostFeedback" = Relationship(back_populates="attachments")


class ArguePostFeedback(SQLModel, table=True):
    __tablename__ = 'argue_post_feedback'

    id: int | None = Field(default=None, primary_key=True)
    argue_post_id: int = Field(foreign_key="argue_post.id")
    content: str | None = Field(default=None, nullable=True)
    score: float | None = Field(default=None, nullable=True)
    marker_username: str = Field(foreign_key="profile.username")
    create_time: datetime | None = Field(default=None, nullable=True)

    argue_post: "ArguePost" = Relationship(back_populates="feedback")
    marker: "Profile" = Relationship()
    attachments: list["ArguePostFeedbackAttachment"] = Relationship(back_populates="argue_post_feedback")
