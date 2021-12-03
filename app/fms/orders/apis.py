import logging
from operator import attrgetter
import re
from typing import NewType
from humanfriendly.terminal import output
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.sqltypes import REAL
from app.models.product import Product
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.orders import Order
from app import db
from sqlalchemy import and_
from utils import vntime

class OrderApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order")


class Test(Resource):
    def get(self):
        datas = Order.query.all()
        output = []
        for data in datas:
            dataDict = data.__dict__
            dataDict.pop("_sa_instance_state")
            output.append(dataDict)
        return output
class OrderTypeApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('status')
        args = parser.parse_args()
        dataFilter = []

        if args['status']:
            dataFilter.append(Order.status == args['status'])
        
        datas = Order.query.filter(and_(*dataFilter)).all() #sua datas
        output =[]
        for data in datas:
            if data.active == "deactive":
                continue
            else:
                dataDict = data.__dict__
                dataDict.pop("_sa_instance_state")
                output.append(dataDict)
        return output



class OrderDetailsApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')

        args = parser.parse_args()
        dataFilter = [] 

        if args["id"]:
            dataFilter.append(Order.id == args['id'])

        datas = Order.query.filter(and_(*dataFilter)).all()

        output = []
        for data in datas:
            if data.active == "deactive":
                continue
            else:
                dataDict = data.__dict__
                dataDict.pop("_sa_instance_state")
                output.append(dataDict)
        return output

class DeleteOrder(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        if args['id'] != "0":
            order = Order.query.get(args['id'])

            order.active = "deactive" # true False
            db.session.add(order)
            db.session.commit()
            return order.active

     