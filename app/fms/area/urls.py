from app import api 
from .apis import *
from .fe_configure import AreafigureApi

api.add_resource(
    AreaApi,
    '/area'
)

api.add_resource(
    AreafigureApi, 
    '/area/filter',      # replace area to module name
    '/area/post',        # replace area to module name
    '/area/patch',       # replace area to module name
    '/area/delete'       # replace area to module name
)
