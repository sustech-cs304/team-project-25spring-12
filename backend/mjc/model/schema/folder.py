from pydantic import BaseModel


class FolderPageItem(BaseModel):
    id: int
    name: str


class FolderBase(BaseModel):
    index: int
    name: str


class Folder(FolderBase):
    id: int | None = None
    pages: list[FolderPageItem]


class FolderCreate(FolderBase):
    class_id: int
    index: int  # 左侧栏中的顺序
    name: str | None = None
    order: list[int] | None = None
    visible: bool | None = True


class FolderUpdate(FolderBase):
    id: int
    index: int
    name: str | None = None
    order: list[int] | None = None
    visible: bool | None = True
