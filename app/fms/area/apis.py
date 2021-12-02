import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.area import Area

class AreaApi(BaseApiPagination):
    """
    URL: /area
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Area, "/area")
