import uuid
from typing import Type
from datetime import datetime

from pydantic import BaseModel

from mjc.model.schema.assignment import Feedback, SubmittedAssignment
from mjc.model.schema.common import File
from mjc.model.schema.user import Profile


class WidgetBase(BaseModel):
    title: str
    index: int
    type: str
    create_time: datetime | None = None
    update_time: datetime | None = None
    editor: Profile | None = None
    visible: bool


class WidgetCreate(BaseModel):
    page_id: int


class WidgetUpdate(BaseModel):
    id: int


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
    submit_type: str
    submitted_assignment: list["SubmittedAssignment"] | None = None
    status: str
    ddl: datetime
    score: float | None = None
    max_score: float
    feedback: Feedback | None = None
    test_case: Type["TestCase"] | None = None


class AssignmentWidgetCreate(WidgetBase):
    index: int
    content: str | None = None
    submit_type: str
    ddl: datetime
    max_score: float
    page_id: int
    visible: bool | None = True


class AssignmentWidgetUpdate(WidgetBase):
    id: int
    content: str | None = None
    submit_type: str
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
    pdf_file: uuid.UUID
    page_id: int
    visible: bool | None = True


class NotePdfWidgetUpdate(WidgetBase):
    id: int
    pdf_file: uuid.UUID
    visible: bool | None = True
    content: str | None = None


class WidgetAttachmentCreate(BaseModel):
    widget_id: int
    file_id: uuid.UUID


class TestCaseBase(BaseModel):
    max_cpu_time: int | None = 1000
    max_memory: int | None = 134217728


class TestPoint(BaseModel):
    stripped_output_md5: str
    output_size: int
    input_name: str
    input_size: int
    output_name: str


class TestCaseInfo(BaseModel):
    spj: bool | None = False
    test_cases: dict[str, TestPoint]


class TestCase(TestCaseBase):
    id: int
    info: TestCaseInfo | None = None


class TestCaseCreate(TestCaseBase):
    file_id: uuid.UUID
    widget_id: int


class TestCaseUpdate(TestCase):
    file_id: uuid.UUID | None = None