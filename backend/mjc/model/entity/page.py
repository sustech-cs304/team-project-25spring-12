from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from mjc.model.entity.course import Class
    from mjc.model.entity.widget import Widget
    from mjc.model.entity.folder import Folder


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

    folder: "Folder" = Relationship(back_populates="pages")
    class_: "Class" = Relationship(back_populates="pages")
