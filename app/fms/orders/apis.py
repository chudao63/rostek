import re
from typing import NewType
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.orders import Order
from app import db
class OrderApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order")

class ChangeStateOrderApi(Resource):
    def post(self):
        data = request.get_json(force= True)
        newOrder = Order(start_time = data["start_time"], end_time = data["end_time"], status = "status",robot = data["robot"], mission = data["mission"], priority = data["priority"], note = data["note"])
        db.session.add(newOrder)
        db.session.commit()
        return "Them thanh cong"