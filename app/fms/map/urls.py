from app import api
from .apis import *
from .fe_configure import MapConfigureApi

api.add_resource(
    MapApiBase,
    '/map'
)
api.add_resource(
    MapConfigureApi, 
    '/map/filter',      # replace map to module name
    '/map/post',        # replace map to module name
    '/map/patch',       # replace map to module name
    '/map/delete'       # replace map to module name
)

api.add_resource(
    UploadMapApi,
    '/upload'
)

api.add_resource(
    DisplayMapApi,
    '/display'
)

api.add_resource(
    DeleteImageApi,
    '/deleteimage'
)

api.add_resource(
    ActiveMapDataApi,  
    '/map_data_active',
)


api.add_resource(
    MapDataApi,
    '/mapdata'
)
