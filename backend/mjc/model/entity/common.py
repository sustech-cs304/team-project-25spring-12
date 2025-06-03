import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.user import Profile


class Visibility(str, Enum):
    public = 'public'
    in_class = 'in_class'


class LocalResourceFile(SQLModel, table=True):
    """
    课程资源
    """
    __tablename__ = 'local_resource_file'

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    upload_time: datetime | None = Field(default=None, nullable=True)
    uploader_username: str | None = Field(foreign_key="profile.username")
    filename: str = Field(nullable=False)
    system_path: str = Field(nullable=False)
    visibility: Visibility = Field(default=Visibility.in_class, sa_column=Column(SQLEnum(Visibility)))
    is_deleted: bool = Field(default=False, nullable=False)

    uploader: "Profile" = Relationship()