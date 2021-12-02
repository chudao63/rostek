from app import api
from .apis import *
from .fe_configure import ProductConfigureApi

api.add_resource(
    ProductApi,
    '/product'
)


api.add_resource(
    ProductConfigureApi, 
    '/product/filter',      # replace product to module name
    '/product/post',        # replace product to module name
    '/product/patch',       # replace product to module name
    '/product/delete'       # replace product to module name
)
