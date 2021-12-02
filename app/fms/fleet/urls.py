from app import api 
from .apis import *
from .fe_configure import FleetConfigureApi


api.add_resource(
    FleetApi,
    '/fleet'
)

api.add_resource(
    FleetConfigureApi, 
    '/neworder/filter',      # replace neworder to module name
    '/neworder/post',        # replace neworder to module name
    '/neworder/patch',       # replace neworder to module name
    '/neworder/delete'       # replace neworder to module name
)
