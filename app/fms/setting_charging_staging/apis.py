from importlib import import_module
from app.models.setting_charging_staging import SettingChargingStaging
from app import db
from utils.apimodel import BaseApiPagination, ApiBase
from utils.common import create_response_message


class SettingChargingStagingBaseApi(BaseApiPagination):
    def __init__(self):
        BaseApiPagination.__init__(self, SettingChargingStaging, "/setting-charging-staging-base")