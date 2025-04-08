import uuid

from pydantic import BaseModel
from ..entity import Visibility


class File(BaseModel):
    id: uuid.UUID
    file_name: str
    visibility: Visibility
    url: str