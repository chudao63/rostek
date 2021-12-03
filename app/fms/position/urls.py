from app import api
from .apis import *
from .fe_configure import PositionConfigureApi

api.add_resource(
    PositionApi,
    '/position'
)


api.add_resource(
    PositionConfigureApi, 
    '/position/filter',      # replace location to module name
    '/position/post',        # replace location to module name
    '/position/patch',       # replace location to module name
    '/position/delete'       # replace location to module name
)
