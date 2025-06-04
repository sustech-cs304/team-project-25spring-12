import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, ARRAY
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.assignment import SubmittedAssignment
    from mjc.model.entity.common import LocalResourceFile
    from mjc.model.entity.page import Page
    from mjc.model.entity.user import Profile


class WidgetType(str, Enum):
    note_pdf = 'notepdf'
    doc = 'doc'
    assignment = 'assignment'


class WidgetAttachment(SQLModel, table=True):
    """
    用于管理系统中 Widget 使用的文件
    """
    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(default=None, foreign_key="local_resource_file.id")
    widget_id: int = Field(foreign_key="widget.id")
    is_deleted: bool = Field(default=False, nullable=False)

    widget: "Widget" = Relationship(back_populates="attachments")
    file: "LocalResourceFile" = Relationship()


class Widget(SQLModel, table=True):
    """
    页面中的控件，可以自由组合
    """
    id: int | None = Field(default=None, primary_key=True)
    title: str | None
    index: int = Field(nullable=False)
    type: WidgetType = Field(sa_column=Column(SQLEnum(WidgetType)))
    create_time: datetime | None
    update_time: datetime | None
    editor_username: str = Field(nullable=True, foreign_key="profile.username")
    content: str | None
    page_id: int = Field(foreign_key="page.id")
    is_deleted: bool = Field(default=False, nullable=False)
    visible: bool = Field(default=False, nullable=False)

    editor: "Profile" = Relationship()  # 此处通过 widget 不应能改变 profile，不加 back_populates
    attachments: list[WidgetAttachment] = Relationship(back_populates="widget")
    page: "Page" = Relationship(back_populates="widgets")

    # 对应到具体的 Widget 内容
    note_pdf_widget: "NotePDFWidget" = Relationship(back_populates="widget")
    assignment_widget: "AssignmentWidget" = Relationship(back_populates="widget")


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    page: int
    x: int
    y: int
    text: str
    create_time: datetime | None
    update_time: datetime | None
    editor_username: str = Field(nullable=True, foreign_key="profile.username")
    note_pdf_widget_id: int = Field(foreign_key="note_pdf_widget.id")
    is_deleted: bool = Field(default=False, nullable=False)

    editor: "Profile" = Relationship()  # 此处通过 note 不应能改变 profile，不加 back_populates
    note_pdf_widget: "NotePDFWidget" = Relationship(back_populates="notes")


class NotePDFWidget(SQLModel, table=True):
    """
    NotePDF Widget 存储的数据
    """
    __tablename__ = 'note_pdf_widget'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    pdf_file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")

    widget: "Widget" = Relationship(back_populates="note_pdf_widget")
    notes: list[Note] = Relationship(back_populates="note_pdf_widget")
    pdf_file: "LocalResourceFile" = Relationship()


class SubmitType(str, Enum):
    """
    作业可选的提交类型
    """
    text = 'text'
    file = 'file'
    code = 'code'


class TestCase(SQLModel, table=True):
    """
    用于 OJ 评测的 TestCase
    """
    __tablename__ = 'test_case'

    id: int | None = Field(default=None, primary_key=True)
    max_cpu_time: int = Field(default=1000)
    max_memory: int = Field(default=134217728)
    info: str = Field(nullable=True)

    assignment_widget: "AssignmentWidget" = Relationship(back_populates="test_case")


class AssignmentWidget(SQLModel, table=True):
    """
    Assignment Widget 存储的数据
    """
    __tablename__ = 'assignment_widget'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    submit_type: SubmitType = Field(sa_column=Column(SQLEnum(SubmitType)))
    ddl: datetime
    max_score: float
    test_case_id: int = Field(foreign_key="test_case.id", nullable=True)

    widget: "Widget" = Relationship(back_populates="assignment_widget")
    submitted_assignments: list["SubmittedAssignment"] = Relationship(back_populates="assignment_widget")
    test_case: "TestCase" = Relationship(back_populates="assignment_widget")