from app import api 
from .apis import SettingCollisionAvoidanceBaseApi
from .fe_configure import SettingColliAvoidanceConfigureApi


api.add_resource(
    SettingCollisionAvoidanceBaseApi,
    '/setting-collision-avoidance-base'
)


api.add_resource(
    SettingColliAvoidanceConfigureApi, 
    '/setting-collision-avoidance-base/filter',      # replace setting-collision-avoidance-base to module name
    '/setting-collision-avoidance-base/post',        # replace setting-collision-avoidance-base to module name
    '/setting-collision-avoidance-base/patch',       # replace setting-collision-avoidance-base to module name
    '/setting-collision-avoidance-base/delete'       # replace setting-collision-avoidance-base to module name
)

