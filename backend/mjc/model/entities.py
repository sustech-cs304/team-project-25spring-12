from datetime import datetime
from enum import Enum

from sqlmodel import Column, Field, SQLModel, Relationship, Enum as SQLEnum


class User(SQLModel, table=True):
    """
    用户实体，主要用来存储用户的安全信息
    """
    __tablename__ = 'mjc_user'  # PostgreSQL 中的 user 表可能会冲突

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True, unique=True)
    encoded_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)

    profile: "Profile" = Relationship(back_populates="user")


class ClassTeacherLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class ClassTeachingAssistantLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class ClassStudentLink(SQLModel, table=True):
    class_id: int = Field(default=None, foreign_key="class.id", primary_key=True)
    username: str = Field(default=None, foreign_key='profile.username', primary_key=True)


class Profile(SQLModel, table=True):
    """
    用户个人资料
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    department: str
    email: str

    username: str = Field(nullable=False, foreign_key="mjc_user.username", unique=True)
    user: User = Relationship(back_populates="profile")
    teacher_classes: list["Class"] = Relationship(back_populates="teacher_classes", link_model=ClassTeacherLink)
    teaching_assistant_classes: list["Class"] = Relationship(back_populates="teaching_assistant_classes", link_model=ClassTeachingAssistantLink)
    student_classes: list["Class"] = Relationship(back_populates="student_classes", link_model=ClassStudentLink)


class SyllabusFile(SQLModel, table=True):
    """
    用于管理系统中 Class 所使用的教学大纲的文件
    """
    id: int | None = Field(default=None, primary_key=True)
    file_name: str | None
    url: str = Field(nullable=False)


class Class(SQLModel, table=True):
    """
    课程
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    course_code: str = Field(nullable=False)
    semester: str
    lecturer: str
    location: str
    time: datetime
    syllabus: str  # URL

    teachers: list["Profile"] = Relationship(back_populates="teacher_classes", link_model=ClassTeacherLink)
    teaching_assistants: list["Profile"] = Relationship(back_populates="teaching_assistant_classes", link_model=ClassTeachingAssistantLink)
    students: list["Profile"] = Relationship(back_populates="student_classes", link_model=ClassStudentLink)
    folders: list["Folder"] = Relationship()
    pages: list["Page"] = Relationship()


class Folder(SQLModel, table=True):
    """
    课程页面集合
    """
    id: int | None = Field(default=None, primary_key=True)
    folder_name: str
    index: int
    class_id: int = Field(foreign_key="class.id")

    pages: list["Page"] = Relationship(back_populates="folder")
    class_: "Class" = Relationship(back_populates="folders")


class Page(SQLModel, table=True):
    """
    页面，用于管理 Widgets
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    widgets: list["Widget"] = Relationship(back_populates="page")
    folder_id: int | None = Field(default=None, foreign_key="folder.id")
    class_id: int = Field(foreign_key="class.id")
    index: int

    folder: Folder = Relationship(back_populates="pages")
    class_: "Class" = Relationship(back_populates="pages")


class WidgetType(str, Enum):
    note_pdf = 'notepdf'
    doc = 'doc'
    assignment = 'assignment'


class WidgetAttachment(SQLModel, table=True):
    """
    用于管理系统中 Widget 使用的文件
    """
    id: int | None = Field(default=None, primary_key=True)
    file_name: str | None
    url: str = Field(nullable=False)
    upload_time: datetime | None
    uploader_username: str | None = Field(nullable=False, foreign_key="profile.username")
    widget_id: int = Field(foreign_key="widget.id")

    uploader: "Profile" = Relationship()
    widget: "Widget" = Relationship(back_populates="attachments")


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
    editor_username: str = Field(nullable=True, foreign_key="profile.username")
    note_pdf_widget_id: int = Field(foreign_key="note_pdf_widget.id")

    editor: "Profile" = Relationship()  # 此处通过 note 不应能改变 profile，不加 back_populates
    note_pdf_widget: "NotePDFWidget" = Relationship(back_populates="notes")


class NotePDFWidget(SQLModel, table=True):
    """
    NotePDF Widget 存储的数据
    """
    __tablename__ = 'note_pdf_widget'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    pdf_file: str

    widget: "Widget" = Relationship(back_populates="note_pdf_widget")
    notes: list[Note] = Relationship(back_populates="note_pdf_widget")


class SubmitType(str, Enum):
    """
    作业可选的提交类型
    """
    text = 'text'
    file = 'file'
    code = 'code'


class AssignmentWidget(SQLModel, table=True):
    """
    Assignment Widget 存储的数据
    """
    __tablename__ = 'assignment_widget'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    submit_types: list[SubmitType] = Field(sa_column=Column(SQLEnum(SubmitType)))
    ddl: datetime
    max_score: int

    widget: "Widget" = Relationship(back_populates="assignment_widget")
    # TODO: 跟已提交的作业的关系