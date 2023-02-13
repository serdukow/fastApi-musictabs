import datetime
from enum import Enum

from pydantic import BaseModel


class StyleKind(str, Enum):
    acoustic = 'acoustic'
    fingerstyle = 'fingerstyle'


class FileBase(BaseModel):
    id: int
    artist: str
    song: str
    kind: StyleKind
    size: str
    mime_type: str
    modification_time: str

    class Config:
        orm_mode = True



