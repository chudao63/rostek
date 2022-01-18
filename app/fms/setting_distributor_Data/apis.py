from app.models.setting_distributor_data import SettingDistributorData
from utils.apimodel import BaseApiPagination



class SettingDistributorDataBaseApi(BaseApiPagination):
    def __init__(self):
        BaseApiPagination.__init__(self, SettingDistributorData, "/setting-distributor-data-base")