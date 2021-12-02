import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.location import Location

class LocationApi(BaseApiPagination):
    """
    URL: /location
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Location, "/location")
