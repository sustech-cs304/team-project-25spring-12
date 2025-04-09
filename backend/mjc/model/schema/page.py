from pydantic import BaseModel


class PageWidgetItem(BaseModel):
    pass


class PageBase(BaseModel):
    name: str
    visible: bool


class Page(PageBase):
    id: int
    index: int
    widgets: list[PageWidgetItem]


class PageCreate(PageBase):
    class_id: int
    folder_id: int
    index: int


class PageUpdate(PageBase):
    id: int
    folder_id : int
    index: int
    order: list[int] | None
