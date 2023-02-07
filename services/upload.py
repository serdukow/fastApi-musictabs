import os
from datetime import datetime


from sqlalchemy.orm import Session
from fastapi import Depends


from settings import UPLOADED_FILES_PATH
from database import get_session
import tables


class UploadService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_to_db(self, **kwargs):
        new_file = tables.Image(
            file_id=kwargs['file_id'],
            name=kwargs['name'],
            tag=kwargs['tag'],
            size=kwargs['file_size'],
            mime_type=kwargs['file'].content_type,
            modification_time=datetime.now()
        )
        self.session.add(new_file)
        self.session.commit()
        return new_file

    def get_file_size(filename, path: str = None):
        file_path = f'{UPLOADED_FILES_PATH}{filename}'
        if path:
            file_path = f'{path}{filename}'
        return os.path.getsize(file_path)

    def format_filename(file, file_id=None, name=None):
        # Split filename and extention
        filename, ext = os.path.splitext(file.filename)

        # Rename file
        if name is None:
            filename = str(file_id)
        else:
            filename = name

        return filename + ext

    async def save_file_to_uploads(file, filename):
        with open(f'{UPLOADED_FILES_PATH}{filename}', "wb") as uploaded_file:
            file_content = await file.read()
            uploaded_file.write(file_content)
            uploaded_file.close()













