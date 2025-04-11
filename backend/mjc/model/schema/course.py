from datetime import datetime

from pydantic import BaseModel

from backend.mjc.model.schema.common import File
from backend.mjc.model.entity import ClassRole


class ClassBase(BaseModel):
    name: str
    course_code: str
    semester: str | None = None
    lecturer: str | None = None
    location: str | None = None
    time: str | None = None


class ClassCard(ClassBase):
    id: int
    role: str | None


class Class(ClassBase):
    id: int
    syllabus: File | None
    role: ClassRole | None


class ClassCreate(ClassBase):
    semester_id: int
    syllabus: File | None
    template_id: int | None = None


class ClassUpdate(ClassBase):
    id: int
    semester_id: int
    syllabus: File | None


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
    assignment_id: int
    assignment_name: str
    ddl: datetime