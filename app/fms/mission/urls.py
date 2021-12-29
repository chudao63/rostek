from app import api
from .apis import *
from .fe_configure import MissionConfigureApi

api.add_resource(
    MissionBaseApi,
    '/mission-base'
)

api.add_resource(
    MissionConfigureApi, 
    '/mission-base/filter',      # replace mission to module name
    '/mission-base/post',        # replace mission to module name
    '/mission-base/patch',       # replace mission to module name
    '/mission-base/delete'       # replace mission to module name
)

api.add_resource(
    MissionApi,
    '/mission'
)

