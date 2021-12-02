from app import api
from .apis import *
from .fe_configure import LocationConfigureApi

api.add_resource(
    LocationApi,
    '/location'
)


api.add_resource(
    LocationConfigureApi, 
    '/location/filter',      # replace location to module name
    '/location/post',        # replace location to module name
    '/location/patch',       # replace location to module name
    '/location/delete'       # replace location to module name
)
