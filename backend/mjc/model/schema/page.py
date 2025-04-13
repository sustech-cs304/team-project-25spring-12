from pydantic import BaseModel

from backend.mjc.model.schema.widget import AssignmentWidget, NotePdfWidget, DocWidget


class PageBase(BaseModel):
    name: str
    visible: bool


class Page(PageBase):
    id: int
    index: int
    widgets: list[AssignmentWidget | NotePdfWidget | DocWidget]


class PageCreate(PageBase):
    class_id: int
    folder_id: int | None = None
    index: int
    visible: bool | None = True


class PageUpdate(PageBase):
    id: int
    folder_id : int | None = None
    index: int
    order: list[int] | None = None
    visible: bool | None = True
