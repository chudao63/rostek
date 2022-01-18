from app import api 
from .apis import SettingChargingStagingBaseApi
from .fe_configure import SettingChargingStagingConfigureApi


api.add_resource(
    SettingChargingStagingBaseApi,
    '/setting-charging-setting-base'
)


api.add_resource(
    SettingChargingStagingConfigureApi, 
    '/setting-charging-staging/filter',      # replace setting-charging-staging to module name
    '/setting-charging-staging/post',        # replace setting-charging-staging to module name
    '/setting-charging-staging/patch',       # replace setting-charging-staging to module name
    '/setting-charging-staging/delete'       # replace setting-charging-staging to module name
)

