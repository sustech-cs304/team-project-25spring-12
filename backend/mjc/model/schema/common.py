from pydantic import BaseModel


class File(BaseModel):
    filename: str
    url: str