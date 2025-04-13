from datetime import datetime

from pydantic import BaseModel

from backend.mjc.model.schema.assignment import Feedback
from backend.mjc.model.schema.common import File
from backend.mjc.model.schema.user import Profile


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
    feedback: Feedback | None = None


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