from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.course import Class
    from mjc.model.entity.page import Page


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
