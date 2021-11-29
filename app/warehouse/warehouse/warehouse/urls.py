from .apis import WarehouseApi
from .fe_configure import ModuleConfigureApi
from app import api

api.add_resource(
    WarehouseApi, 
    '/warehouse',
)

api.add_resource(
    ModuleConfigureApi, 
    '/warehouse/filter', # Get filter 
    '/warehouse/post',   # Get atr post
    '/warehouse/patch',   # Get atr patch
    '/warehouse/delete'
)
