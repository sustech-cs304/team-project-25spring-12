from datetime import datetime

from pydantic import BaseModel

from common import File
from user import Profile


class ClassBase(BaseModel):
    name: str
    course_code: str
    semester: str
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
    pass


class ClassUpdate(ClassBase):
    id: int


class FolderPageItem(BaseModel):
    id: int
    name: str


class FolderBase(BaseModel):
    index: int
    name: str


class Folder(FolderBase):
    id: int
    pages: list[FolderPageItem]


class FolderCreate(FolderBase):
    class_id: int
    index: int  # 左侧栏中的顺序
    name: str | None
    order: list[int] | None


class FolderUpdate(FolderBase):
    id: int
    index: int
    name: str | None
    order: list[int] | None


class PageWidgetItem(BaseModel):
    pass


class PageBase(BaseModel):
    name: str


class Page(PageBase):
    id: int
    index: int
    widgets: list[PageWidgetItem]


class PageCreate(PageBase):
    class_id: int
    folder_id: int
    index: int


class PageUpdate(PageBase):
    id: int
    folder_id : int
    index: int
    order: list[int] | None


class WidgetBase(BaseModel):
    title: str
    index: int
    type: str
    create_time: datetime
    update_time: datetime
    editor: Profile | None


class DocWidget(WidgetBase):
    id: int
    content: str | None
    attachments: list[File] | None


class DocWidgetCreate(WidgetBase):
    index: int
    content: str | None
    attachments: list[File] | None


class DocWidgetUpdate(DocWidget):
    pass


class AssignmentWidget(WidgetBase):
    id: int
    content: str | None
    attachments: list[File] | None
    submit_type: list[str]
    submitted_assignment: list["SubmittedAssignment"] | None
    status: str
    ddl: datetime
    score: float | None
    max_score: float
    feedback: str | None


class AssignmentWidgetCreate(WidgetBase):
    index: int
    content: str | None
    attachments: list[File] | None
    submit_type: list[str]
    ddl: datetime
    max_score: float


class AssignmentUpdate(WidgetBase):
    id: int
    content: str | None
    attachments: list[File] | None
    submit_type: list[str]
    ddl: datetime
    max_score: float


class Code(BaseModel):
    content: str
    language: str


class SubmittedAssignment(BaseModel):
    id: int
    content: str
    attachments: list[File]
    code: Code
    submitted_time: datetime


class NoteBase(BaseModel):
    page: int
    x: int
    y: int
    text: str


class Note(NoteBase):
    id: int
    editor: Profile


class NotePdfWidget(WidgetBase):
    id: int
    pdf_file: File
    notes: list[Note] | None


class NotePdfWidgetCreate(WidgetBase):
    index: int
    pdf_file: File


class NotePdfUpdate(WidgetBase):
    id: int
    pdf_file: File


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