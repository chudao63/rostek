from app import api
from .apis import *
from .fe_configure import PriorityConfigureApi

api.add_resource(
    PriorityApi,
    '/priority'
)


api.add_resource(
    PriorityConfigureApi, 
    '/priority/filter',      # replace priority to module name
    '/priority/post',        # replace priority to module name
    '/priority/patch',       # replace priority to module name
    '/priority/delete'       # replace priority to module name
)
