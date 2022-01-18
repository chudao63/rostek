from app import api 
from .apis import  SettingDistributorDataBaseApi
from .fe_configure import SettingDistributorDataConfigureApi


api.add_resource(
    SettingDistributorDataBaseApi,
    '/setting-distributor-data-base'
)


api.add_resource(
    SettingDistributorDataConfigureApi, 
    '/setting-distributor-data-base/filter',      # replace setting-distributor-data-base to module name
    '/setting-distributor-data-base/post',        # replace setting-distributor-data-base to module name
    '/setting-distributor-data-base/patch',       # replace setting-distributor-data-base to module name
    '/setting-distributor-data-base/delete'       # replace setting-distributor-data-base to module name
)

