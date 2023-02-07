import datetime


from pydantic import BaseModel


class FileBase(BaseModel):
    id: int
    file_id: int
    name: str
    tag: str
    size: str
    mime_type: str
    modification_time: str

    class Config:
        orm_mode = True



