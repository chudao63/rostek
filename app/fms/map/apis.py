import re
from sqlalchemy.sql.sqltypes import REAL
from app.models.map import Maps
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.groups import 
import os, sys
from flask import send_from_directory

class MapsApi(BaseApiPagination):
    """
    URL: /map
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Maps, "/map")


class UploadFileApi(Resource):
    def post(self):
        pass