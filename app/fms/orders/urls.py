from app import api
from .apis import *
from .fe_configure import OrderConfigureApi

api.add_resource(
    OrderApi,
    '/order'
)

api.add_resource(
    OrderTypeApi,
    '/orders'
)

api.add_resource(
    DeleteOrder,
    '/deleteorder'
)
api.add_resource(
    OrderDetailsApi,
    '/orderdetails'
) # sua lai details




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