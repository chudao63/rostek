from app import api
from .apis import *
from .fe_configure import OrderConfigureApi


api.add_resource(
    OrderApi,
    '/order-base'
)

api.add_resource(
    OrderDetailsApi,
    '/order'
)

api.add_resource(
    OrdersApi,
    '/orders'
)

api.add_resource(
    SetActivation,
    '/setactivation'
)


api.add_resource(
    OrderConfigureApi, 
    '/order/filter',      # replace order to module name
    '/order/post',        # replace order to module name
    '/order/patch',       # replace order to module name
    '/order/delete'       # replace order to module name
)


api.add_resource(
    Test,
    '/test'
)