from app import api 
from .apis import *
from .fe_configure import StepconfigureApi

api.add_resource(
    StepApiBase,
    '/step-base'
)

api.add_resource(
    StepconfigureApi, 
    '/step-base/filter',      # replace step-base to module name
    '/step-base/post',        # replace step-base to module name
    '/step-base/patch',       # replace step-base to module name
    '/step-base/delete'       # replace step-base to module name
)


api.add_resource(
    StepApi,
    '/step'
)
