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

    return RedirectResponse('post', status_code=status.HTTP_302_FOUND)


@router.get("/")
def home(
        request: Request
):
    return main.templates.TemplateResponse('home.html', context={'request': request})


