from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.course import Class
from mjc.model.entity.course import ClassTeacherLink, ClassTeachingAssistantLink, ClassStudentLink


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
