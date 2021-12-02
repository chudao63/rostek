from app import api
from .apis import *
from .fe_configure import GroupsConfigureApi

api.add_resource(
    GroupsApi,
    '/groups'
)



api.add_resource(
    GroupsConfigureApi, 
    '/groups/filter',      # replace groups to module name
    '/groups/post',        # replace groups to module name
    '/groups/patch',       # replace groups to module name
    '/groups/delete'       # replace groups to module name
)
