from app import api
from .apis import *



api.add_resource(
    DownloadLogFileApi,
    '/download-log'
)
