from .apis import BinSizeApi # replace example to module name
from .fe_configure import BinSizeConfigureApi
from app import api

api.add_resource(
    BinSizeApi,             # replace example to module name
    '/bin_size',             # replace example to module name
)

api.add_resource(
    BinSizeConfigureApi, 
    '/bin_size/filter',      # replace example to module name
    '/bin_size/post',        # replace example to module name
    '/bin_size/patch',       # replace example to module name
    '/bin_size/delete'       # replace example to module name
)
