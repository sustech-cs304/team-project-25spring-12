from datetime import datetime

from pydantic import BaseModel

from .common import File


class ClassBase(BaseModel):
    name: str
    course_code: str
    semester: str | None
    lecturer: str | None
    location: str | None
    time: str | None


class ClassCard(ClassBase):
    id: int
    pass


class Class(ClassBase):
    id: int
    syllabus: File | None


class ClassCreate(ClassBase):
    semester_id: int
    syllabus: File | None
    template_id: int | None
    pass


class ClassUpdate(ClassBase):
    id: int
    semester_id: int
    syllabus: File | None


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