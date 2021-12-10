from app import api
from .apis import *
from .fe_configure import MapConfigureApi

api.add_resource(
    MapsApi,
    '/map'
)



api.add_resource(
    MapConfigureApi, 
    '/map/filter',      # replace map to module name
    '/map/post',        # replace map to module name
    '/map/patch',       # replace map to module name
    '/map/delete'       # replace map to module name
)
