import uuid

from pydantic import BaseModel
from mjc.model.entity import Visibility


class FileBase(BaseModel):
    id: uuid.UUID | None = None
    filename: str
    visibility: Visibility


class File(FileBase):
    url: str | None = None


class LocalResourceFileCreate(FileBase):
    id: uuid.UUID
    system_path: str


class Message(BaseModel):
    msg: str


class Code(BaseModel):
    code: str
    language: str
