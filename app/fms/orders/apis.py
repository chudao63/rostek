import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.orders import Order

class OrderApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order")

class ChangeStateOrderApi(Resource):
    def get(self):
        datas = Order.query.all()
        output = []
        for data in datas:
            dataDict = data.__dict__
            dataDict.pop("_sa_stance_state")
            output.append(dataDict)
        return output
    def post(self):
        data = request.get_json(force=True)