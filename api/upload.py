
from typing import Optional

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    status,
    Request, Form

)

from services.upload import UploadService
from models.upload import FileBase
import main


router = APIRouter(
    tags=['upload']
)


@router.get("/post")
def form_post(
        request: Request,
):
    return main.templates.TemplateResponse('index.html', context={'request': request})


@router.post('/post', status_code=status.HTTP_200_OK, response_model=FileBase)
async def form_post(
                file_id: int = Form(...),
                name: Optional[str] = Form(...),
                tag: Optional[str] = Form(...),
                file: UploadFile = File(...),
                service: UploadService = Depends()
):
    full_name = UploadService.format_filename(file, file_id, name)

    await UploadService.save_file_to_uploads(file, full_name)

    file_size = UploadService.get_file_size(full_name)

    return service.add_to_db(
        name=name,
        file_id=file_id,
        tag=tag,
        file_size=file_size,
        file=file
    )


