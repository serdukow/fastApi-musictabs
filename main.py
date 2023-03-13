from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from humanize import naturaltime

from api.upload import router as UploadRouter

app = FastAPI(
    title='Music Tabs',
    version='0.0.1'
)

templates = Jinja2Templates(directory="templates/")
app.include_router(UploadRouter)







