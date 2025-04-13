from datetime import datetime
from enum import Enum
import uuid

from sqlmodel import Column, Field, SQLModel, Relationship, Enum as SQLEnum, ARRAY


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


class ClassRole(str, Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'
    TA = 'teaching assistant'
    NONE = ''


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
    teacher_classes: list["Class"] = Relationship(back_populates="teachers", link_model=ClassTeacherLink)
    teaching_assistant_classes: list["Class"] = Relationship(back_populates="teaching_assistants", link_model=ClassTeachingAssistantLink)
    student_classes: list["Class"] = Relationship(back_populates="students", link_model=ClassStudentLink)


class SyllabusFile(SQLModel, table=True):
    """
    用于管理系统中 Class 所使用的教学大纲的文件
    """
    id: int | None = Field(default=None, primary_key=True)
    file_name: str | None
    url: str = Field(nullable=False)


class Semester(SQLModel, table=True):
    """
    学期
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)

    classes: list["Class"] = Relationship(back_populates="semester")


class Class(SQLModel, table=True):
    """
    课程
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    course_code: str = Field(nullable=False)
    semester_id: int = Field(default=None, foreign_key="semester.id")
    lecturer: str
    location: str
    time: str
    syllabus_id: uuid.UUID | None = Field(default=None, foreign_key="local_resource_file.id")
    is_deleted: bool = Field(default=False, nullable=False)

    teachers: list["Profile"] = Relationship(back_populates="teacher_classes", link_model=ClassTeacherLink)
    teaching_assistants: list["Profile"] = Relationship(back_populates="teaching_assistant_classes", link_model=ClassTeachingAssistantLink)
    students: list["Profile"] = Relationship(back_populates="student_classes", link_model=ClassStudentLink)
    folders: list["Folder"] = Relationship()
    pages: list["Page"] = Relationship()
    semester: "Semester" = Relationship(back_populates="classes")
    syllabus: "LocalResourceFile" = Relationship()


class Folder(SQLModel, table=True):
    """
    课程页面集合
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    index: int
    class_id: int = Field(foreign_key="class.id")
    is_deleted: bool = Field(default=False, nullable=False)
    visible: bool = Field(default=True, nullable=False)

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
    is_deleted: bool = Field(default=False, nullable=False)
    visible: bool = Field(default=True, nullable=False)

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


class AssignmentWidget(SQLModel, table=True):
    """
    Assignment Widget 存储的数据
    """
    __tablename__ = 'assignment_widget'

    id: int | None = Field(default=None, primary_key=True)
    widget_id: int = Field(foreign_key="widget.id")
    submit_types: list[SubmitType] = Field(sa_column=Column(ARRAY(SQLEnum(SubmitType))))
    ddl: datetime
    max_score: float

    widget: "Widget" = Relationship(back_populates="assignment_widget")
    submitted_assignments: list["SubmittedAssignment"] = Relationship(back_populates="assignment")


class Visibility(str, Enum):
    public = 'public'
    in_class = 'in_class'


class LocalResourceFile(SQLModel, table=True):
    """
    课程资源
    """
    __tablename__ = 'local_resource_file'

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    upload_time: datetime | None = Field(default=None, nullable=True)
    uploader_username: str | None = Field(foreign_key="profile.username")
    filename: str = Field(nullable=False)
    system_path: str = Field(nullable=False)
    visibility: Visibility = Field(default=Visibility.in_class, sa_column=Column(SQLEnum(Visibility)))
    is_deleted: bool = Field(default=False, nullable=False)

    uploader: "Profile" = Relationship()


class SubmittedAssignmentAttachment(SQLModel, table=True):
    __tablename__ = 'submitted_assignment_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    submitted_assignment_id: int = Field(foreign_key="submitted_assignment.id")

    submitted_assignment: "SubmittedAssignment" = Relationship(back_populates="submitted_assignments")
    file: "LocalResourceFile" = Relationship()


class FeedbackAttachment(SQLModel, table=True):
    __tablename__ = 'feedback_attachment'

    id: int | None = Field(default=None, primary_key=True)
    file_id: uuid.UUID = Field(foreign_key="local_resource_file.id")
    feedback_id: int = Field(foreign_key="submitted_assignment_feedback.id")

    feedback: "SubmittedAssignmentFeedback" = Relationship(back_populates="attachments")
    file:"LocalResourceFile" = Relationship()


class SubmittedAssignmentFeedback(SQLModel, table=True):
    __tablename__ = 'submitted_assignment_feedback'
    id: int | None = Field(default=None, primary_key=True)
    score: float
    content: str | None = Field(nullable=False)
    create_time: datetime | None = Field(default=None, nullable=True)
    submitted_assignment_id: int = Field(foreign_key="submitted_assignment.id")
    maker: str | None = Field(foreign_key="profile.username")

    attachments: list["FeedbackAttachment"] = Relationship(back_populates="feedback")
    submitted_assignment: "SubmittedAssignment" = Relationship(back_populates="feedback")


class SubmittedAssignment(SQLModel, table=True):
    __tablename__ = 'submitted_assignment'

    id: int | None = Field(default=None, primary_key=True)

    create_time: datetime | None = Field(default=None, nullable=True)
    assignment_widget_id: int = Field(foreign_key="assignment_widget.id")
    username: str | None = Field(foreign_key="profile.username")
    content: str | None = Field(default=None, nullable=True)
    code: str | None = Field(default=None, nullable=True)
    language: str | None = Field(default=None, nullable=True)
    marked: str | None = Field(default=None, nullable=True)

    feedback: "SubmittedAssignmentFeedback" = Relationship(back_populates="submitted_assignment")
    assignment_widget: "AssignmentWidget" = Relationship(back_populates="submitted_assignments")
    attachment: list["SubmittedAssignmentAttachment"] = Relationship(back_populates="submitted_assignment")
