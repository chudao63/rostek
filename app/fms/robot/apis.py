
from app.models.robot import Robot
from utils.apimodel import BaseApiPagination


class RobotApi(BaseApiPagination):

    def __init__(self):
        BaseApiPagination.__init__(self, Robot, "/robot")