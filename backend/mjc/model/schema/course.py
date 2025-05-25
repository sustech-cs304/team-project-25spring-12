from datetime import datetime

from pydantic import BaseModel

from mjc.model.schema.common import File
from mjc.model.entity.course import ClassRole


class ClassBase(BaseModel):
    name: str
    course_code: str
    semester: str | None = None
    lecturer: str | None = None
    location: str | None = None
    time: str | None = None


class ClassCard(ClassBase):
    id: int
    role: str | None = None


class Class(ClassBase):
    id: int
    syllabus: File | None = None
    role: ClassRole | None = None


class ClassCreate(ClassBase):
    semester_id: int
    syllabus: File | None = None
    template_id: int | None = None


class ClassUpdate(ClassBase):
    id: int
    semester_id: int
    syllabus: File | None = None


class SemesterBase(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime


class Semester(SemesterBase):
    id: int


class SemesterCreate(SemesterBase):
    pass


class SemesterUpdate(SemesterBase):
    id: int


class Announcement(BaseModel):
    class_id: int
    class_name: str
    title: str
    page_id: str


class DDL(BaseModel):
    class_id: int
    class_name: str
    widget_id: int
    widget_title: str
    page_id: int
    page_name: str
    ddl: datetime
    course_code: str


class ClassUserRole(BaseModel):
    username: str
    role: ClassRole


class ClassUserEnroll(BaseModel):
    class_id: int
    usernames: list[str]
    role: ClassRole


class ClassUserUpdate(BaseModel):
    class_id: int
    username: str
    role: ClassRole


class ClassUserRoleName(ClassUserRole):
    username: str
    name: str
    role: ClassRole