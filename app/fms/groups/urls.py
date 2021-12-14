from app import api
from .apis import *
from .fe_configure import GroupConfigureApi

api.add_resource(
    GroupApi,
    '/groups'
)



api.add_resource(
    GroupConfigureApi, 
    '/group/filter',      # replace groups to module name
    '/group/post',        # replace groups to module name
    '/group/patch',       # replace groups to module name
    '/group/delete'       # replace groups to module name
)
