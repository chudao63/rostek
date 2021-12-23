from app import api
from .apis import *
from .fe_configure import MissionConfigureApi

api.add_resource(
    MissionApi,
    '/mission'
)

api.add_resource(
    MissionDetailApi,
    '/mission-detail'
)

api.add_resource(
    MissionConfigureApi, 
    '/mission/filter',      # replace mission to module name
    '/mission/post',        # replace mission to module name
    '/mission/patch',       # replace mission to module name
    '/mission/delete'       # replace mission to module name
)

api.add_resource(
    MissionStepApi,
    '/mission-step'
)

api.add_resource(
CreateMissionApi,
    '/create-mission'
)