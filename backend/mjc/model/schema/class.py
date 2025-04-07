from pydantic import BaseModel

from common import File


class ClassBase(BaseModel):
    id: int
    name: str
    course_code: str
    semester: str
    lecturer: str
    location: str
    time: str


class ClassCard(ClassBase):
    pass


class Class(ClassBase):
    syllabus: File | None