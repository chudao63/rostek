import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from app.models.type_robot import TypeRobot

class TypeRobotApi(BaseApiPagination):
    """
    URL: /typeroobt
    """
    def __init__(self):
        BaseApiPagination.__init__(self, TypeRobot, "/typerobot")
