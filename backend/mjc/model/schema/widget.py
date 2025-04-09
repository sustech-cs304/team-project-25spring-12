from datetime import datetime

from pydantic import BaseModel

from backend.mjc.model.schema.common import File
from backend.mjc.model.schema.user import Profile


class WidgetBase(BaseModel):
    title: str
    index: int
    type: str
    create_time: datetime
    update_time: datetime
    editor: Profile | None
    visible: bool


class DocWidget(WidgetBase):
    id: int
    content: str | None
    attachments: list[File] | None


class DocWidgetCreate(WidgetBase):
    index: int
    content: str | None
    attachments: list[File] | None
    page_id: int


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
    page_id: int


class AssignmentWidgetUpdate(WidgetBase):
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
    page_id: int


class NotePdfWidgetUpdate(WidgetBase):
    id: int
    pdf_file: File
