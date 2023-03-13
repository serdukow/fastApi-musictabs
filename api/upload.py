import sqlite3
from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    status,
    Request,
    Form,
)
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from humanize import naturaltime

from services.upload import UploadService
from models.upload import FileBase
import main


router = APIRouter(
    tags=['upload']
)


@router.get("/post")
def publish_tab(
        request: Request
):
    return main.templates.TemplateResponse('index.html', context={'request': request})


@router.post('/post', status_code=status.HTTP_200_OK, response_model=FileBase)
async def publish_tab(
                artist: Optional[str] = Form(...),
                song: Optional[str] = Form(...),
                kind: Optional[str] = Form(...),
                file: UploadFile = File(...),
                service: UploadService = Depends(),

):
    full_name = UploadService.format_filename(file, song)

    await UploadService.save_file_to_uploads(file, full_name)

    file_size = UploadService.get_file_size(full_name)

    service.add_to_db(
        artist=artist,
        song=song,
        kind=kind,
        file_size=file_size,
        file=file
    )

    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@router.get("/")
def home(
        request: Request,
        search: Optional[str] = None
):

    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    if search:
        cursor.execute('SELECT id, artist, song, kind, size, mime_type, modification_time FROM images WHERE song LIKE ? OR artist LIKE ?',
                       ('%' + search + '%', '%' + search + '%',))
    else:
        cursor.execute('SELECT id, artist, song, kind, size, mime_type, modification_time FROM images')

    data = cursor.fetchall()
    conn.close()
    return main.templates.TemplateResponse('home.html', context={'request': request, "data": data})


@router.get('/home/{tab_id}', response_model=FileBase)
def get_tab(
        tab_id: int,
        service: UploadService = Depends()
):
    return service.get(tab_id)


@router.get("/latest_data")
async def get_latest_data():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    data = cursor.fetchall()
    return JSONResponse(content=data)


@router.post('/delete/{tab_id}')
def delete_row(
        tab_id: int,
        service: UploadService = Depends()
):
    service.delete(tab_id)
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


last_modified_time = datetime.now()


@router.get("/api/get-modification-time")
async def get_modification_time():
    global last_modified_time
    time_ago = naturaltime(datetime.now() - last_modified_time)
    return time_ago