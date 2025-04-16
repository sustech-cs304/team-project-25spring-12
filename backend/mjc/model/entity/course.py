import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, Enum as SQLEnum, Column

if TYPE_CHECKING:
    from mjc.model.entity.common import LocalResourceFile
    from mjc.model.entity.page import Page
    from mjc.model.entity.folder import Folder
    from mjc.model.entity.user import Profile


class ClassRole(str, Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'
    TA = 'teaching assistant'
    NONE = ''


class ClassTeacherLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class ClassTeachingAssistantLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class ClassStudentLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class ClassUserLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)
    role: ClassRole = Field(default=ClassRole.STUDENT, sa_column=Column(SQLEnum(ClassRole)))


class SyllabusFile(SQLModel, table=True):
    """
    用于管理系统中 Class 所使用的教学大纲的文件
    """
    id: int | None = Field(default=None, primary_key=True)
    file_name: str | None
    url: str = Field(nullable=False)


class Semester(SQLModel, table=True):
    """
    学期
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)

    classes: list["Class"] = Relationship(back_populates="semester")


class Class(SQLModel, table=True):
    """
    课程
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    course_code: str = Field(nullable=False)
    semester_id: int = Field(default=None, foreign_key="semester.id")
    lecturer: str
    location: str
    time: str
    syllabus_id: uuid.UUID | None = Field(default=None, foreign_key="local_resource_file.id")
    is_deleted: bool = Field(default=False, nullable=False)

    users: list["Profile"] = Relationship(back_populates="classes", link_model=ClassUserLink)
    folders: list["Folder"] = Relationship()
    pages: list["Page"] = Relationship()
    semester: "Semester" = Relationship(back_populates="classes")
    syllabus: "LocalResourceFile" = Relationship()
