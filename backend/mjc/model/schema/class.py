from datetime import datetime

from pydantic import BaseModel

from common import File
from user import Profile


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


class FolderPageItem(BaseModel):
    id: int
    name: str


class FolderBase(BaseModel):
    id: int
    index: int
    name: str


class Folder(FolderBase):
    pages: list[FolderPageItem]


class PageWidgetItem(BaseModel):
    pass


class Page(BaseModel):
    id: int
    name: str
    index: int
    widgets: list[PageWidgetItem]


class WidgetBase(BaseModel):
    id: int
    title: str
    index: int
    type: str
    create_time: datetime
    update_time: datetime
    editor: Profile


class DocumentWidget(WidgetBase):
    content: str | None
    attachments: list[File] | None


class Code(BaseModel):
    content: str
    language: str


class SubmittedAssignment(BaseModel):
    content: str
    attachments: list[File]
    code: Code
    submitted_time: datetime


class AssignmentWidget(WidgetBase):
    content: str | None
    attachments: list[File] | None
    submit_type: list[str]
    submitted_assignment: list[SubmittedAssignment] | None
    status: str
    ddl: datetime
    score: float | None
    max_score: float
    feedback: str | None


class Note(BaseModel):
    page: int
    x: int
    y: int
    text: str
    editor: Profile


class NotePdfWidget(WidgetBase):
    pdf_file: File
    notes: list[Note] | None


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