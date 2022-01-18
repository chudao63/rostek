from app.models.setting_collision_avoidance import SettingCollisionAvoidance
from utils.apimodel import BaseApiPagination



class SettingCollisionAvoidanceBaseApi(BaseApiPagination):
    def __init__(self):
        BaseApiPagination.__init__(self, SettingCollisionAvoidance, "/setting-collision-avoidance-base")