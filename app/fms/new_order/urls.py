from app import api
from .apis import *
from .fe_configure import NewOrderConfigureApi

api.add_resource(
    NewOrderApi,
    '/neworder'
)


api.add_resource(
    NewOrderConfigureApi, 
    '/neworder/filter',      # replace neworder to module name
    '/neworder/post',        # replace neworder to module name
    '/neworder/patch',       # replace neworder to module name
    '/neworder/delete'       # replace neworder to module name
)
