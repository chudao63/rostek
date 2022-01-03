from flask_restful import Api
from app import api
from .apis import *
from .fe_configure import GroupConfigureApi

api.add_resource(
    GroupApiBase,
    '/group-base'
)

api.add_resource(
    GroupApi,
    '/group'
)

api.add_resource(
    GroupConfigureApi, 
    '/group-base/filter',      # replace group-bases to module name
    '/group-base/post',        # replace group-bases to module name
    '/group-base/patch',       # replace group-bases to module name
    '/group-base/delete'       # replace group-bases to module name
)
