import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.groups import Groups

class GroupsApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Groups, "/groups")
