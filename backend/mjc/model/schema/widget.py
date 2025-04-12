from datetime import datetime

from pydantic import BaseModel

from backend.mjc.model.schema.common import File
from backend.mjc.model.schema.user import Profile


class FeedBack(BaseModel):
    score: float | None = None
    content: str | None = None
    attachments: list[File] | None = None
    create_time: datetime | None = None


class WidgetBase(BaseModel):
    title: str
    index: int
    type: str
    create_time: datetime | None = None
    update_time: datetime | None = None
    editor: Profile | None = None
    visible: bool


class DocWidget(WidgetBase):
    id: int
    content: str | None = None
    attachments: list[File] | None = None


class DocWidgetCreate(WidgetBase):
    index: int
    content: str | None = None
    page_id: int
    visible: bool | None = True


class DocWidgetUpdate(DocWidget):
    visible: bool | None = True


class AssignmentWidget(WidgetBase):
    id: int
    content: str | None = None
    attachments: list[File] | None = None
    submit_types: list[str]
    submitted_assignment: list["SubmittedAssignment"] | None = None
    status: str
    ddl: datetime
    score: float | None = None
    max_score: float
    feedback: FeedBack | None = None


class AssignmentWidgetCreate(WidgetBase):
    index: int
    content: str | None = None
    submit_types: list[str]
    ddl: datetime
    max_score: float
    page_id: int
    visible: bool | None = True


class AssignmentWidgetUpdate(WidgetBase):
    id: int
    content: str | None = None
    submit_types: list[str]
    ddl: datetime
    max_score: float
    visible: bool | None = True


class Code(BaseModel):
    content: str
    language: str


class SubmittedAssignmentBase(BaseModel):
    content: str | None = None
    attachments: list[File] | None = None
    code: Code | None = None


class SubmittedAssignmentCreate(SubmittedAssignmentBase):
    widget_id: int


class SubmittedAssignment(SubmittedAssignmentBase):
    id: int
    submitted_time: datetime
    student: Profile | None = None
    feedback: FeedBack | None = None


class NoteBase(BaseModel):
    page: int
    x: int
    y: int
    text: str


class Note(NoteBase):
    id: int
    editor: Profile
    create_time: datetime | None = None
    update_time: datetime | None = None


class NoteCreate(NoteBase):
    widget_id: int


class NoteUpdate(NoteBase):
    id: int


class NotePdfWidget(WidgetBase):
    id: int
    pdf_file: File
    notes: list[Note] | None = None


class NotePdfWidgetCreate(WidgetBase):
    index: int
    pdf_file: File
    page_id: int
    visible: bool | None = True


class NotePdfWidgetUpdate(WidgetBase):
    id: int
    pdf_file: File
    visible: bool | None = True


class WidgetAttachmentCreate(BaseModel):
    widget_id: int
    file: File