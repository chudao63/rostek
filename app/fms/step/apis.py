import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.step import Step

class StepApi(BaseApiPagination):
    """
    URL: /step
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Step, "/step")
