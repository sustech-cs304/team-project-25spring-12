import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.user import Profile
    from mjc.model.entity.widget import AssignmentWidget
    from mjc.model.entity.common import LocalResourceFile
    from mjc.model.entity.argue import ArguePost


class SubmittedAssignmentAttachment(SQLModel, table=True):
    __tablename__ = 'submitted_assignment_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    submitted_assignment_id: int = Field(foreign_key="submitted_assignment.id")
    is_deleted: bool = Field(default=False, nullable=False)

    submitted_assignment: "SubmittedAssignment" = Relationship(back_populates="attachments")
    file: "LocalResourceFile" = Relationship()


class FeedbackAttachment(SQLModel, table=True):
    __tablename__ = 'feedback_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    feedback_id: int = Field(foreign_key="submitted_assignment_feedback.id")
    is_deleted: bool = Field(default=False, nullable=False)

    feedback: "SubmittedAssignmentFeedback" = Relationship(back_populates="attachments")
    file:"LocalResourceFile" = Relationship()


class SubmittedAssignmentFeedback(SQLModel, table=True):
    __tablename__ = 'submitted_assignment_feedback'
    id: int | None = Field(default=None, primary_key=True)
    score: float
    content: str | None = Field(nullable=False)
    create_time: datetime | None = Field(default=None, nullable=True)
    submitted_assignment_id: int = Field(foreign_key="submitted_assignment.id")
    marker: str | None = Field(foreign_key="profile.username")

    attachments: list["FeedbackAttachment"] = Relationship(back_populates="feedback")
    submitted_assignment: "SubmittedAssignment" = Relationship(back_populates="feedback")


class SubmittedAssignment(SQLModel, table=True):
    __tablename__ = 'submitted_assignment'

    id: int | None = Field(default=None, primary_key=True)

    create_time: datetime | None = Field(default=None, nullable=True)
    assignment_widget_id: int = Field(foreign_key="assignment_widget.id")
    username: str | None = Field(foreign_key="profile.username")
    content: str | None = Field(default=None, nullable=True)
    code: str | None = Field(default=None, nullable=True)
    language: str | None = Field(default=None, nullable=True)
    marked: bool = Field(default=False)

    feedback: "SubmittedAssignmentFeedback" = Relationship(back_populates="submitted_assignment")
    assignment_widget: "AssignmentWidget" = Relationship(back_populates="submitted_assignments")
    attachments: list["SubmittedAssignmentAttachment"] = Relationship(back_populates="submitted_assignment")
    profile: "Profile" = Relationship()
    argue_post: "ArguePost" = Relationship(back_populates="submitted_assignment")
