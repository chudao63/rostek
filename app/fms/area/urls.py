from app import api 
from .apis import *

api.add_resource(
    AreaApi,
    '/area'
)