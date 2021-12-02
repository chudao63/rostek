from app import api
from .apis import *
from .fe_configure import TypeRobotConfigureApi

api.add_resource(
    TypeRobotApi,
    '/typerobot'
)


api.add_resource(
    TypeRobotConfigureApi, 
    '/typerobot/filter',      # replace typerobot to module name
    '/typerobot/post',        # replace typerobot to module name
    '/typerobot/patch',       # replace typerobot to module name
    '/typerobot/delete'       # replace typerobot to module name
)
