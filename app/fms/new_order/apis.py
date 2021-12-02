import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.orders import NewOder

class NewOrderApi(BaseApiPagination):
    """
    URL: /neworder
    """
    def __init__(self):
        BaseApiPagination.__init__(self, NewOder, "/neworder")
