from app import api 
from .apis import *
from .fe_configure import StepconfigureApi

api.add_resource(
    StepApi,
    '/step'
)

api.add_resource(
    StepconfigureApi, 
    '/step/filter',      # replace step to module name
    '/step/post',        # replace step to module name
    '/step/patch',       # replace step to module name
    '/step/delete'       # replace step to module name
)
