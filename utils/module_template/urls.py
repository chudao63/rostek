from .apis import ExampleApi # replace example to module name
from .fe_configure import ModuleConfigureApi
from app import api

api.add_resource(
    ExampleApi,             # replace example to module name
    '/example',             # replace example to module name
)

api.add_resource(
    ModuleConfigureApi, 
    '/example/filter',      # replace example to module name
    '/example/post',        # replace example to module name
    '/example/patch',       # replace example to module name
    '/example/delete'       # replace example to module name
)
