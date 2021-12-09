import logging
from operator import attrgetter
from os import name
import re
from typing import NewType
from humanfriendly.terminal import output
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.sqltypes import REAL
from app.fms.orders.consts import ORDER_STATUS
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
        """
        Trả về thông tin của các lệnh được tìm theo ID và trạng thái của lệnh
        """
        parser = reqparse.RequestParser()
        parser.add_argument('status')
        args = parser.parse_args()
        dataFilter = []

        if args['status']:
            dataFilter.append(Order.status == args['status'])
        datas = Order.query.filter(and_(*dataFilter)).all() #sua datas

        output =[]
        
        for data in datas:
            robotName   = data.robot.name
            missionName = data.mission.name
            jobType = data.mission.type_job

            if data.active == 0:
                continue
            else:
                dataDict = data.__dict__
                dataDict.pop("_sa_instance_state")
                dataDict.pop("robot")
                dataDict.pop("mission")

                dataDict["robot_name"]  = robotName
                dataDict["mision_name"] = missionName
                dataDict["jobType"]     = jobType
                output.append(dataDict)
        return output

class OrdersApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status')
        args = parser.parse_args()
        dataFilter = []


        for orderStatus in ORDER_STATUS:
            if args['status'] == orderStatus.name.lower():
                dataFilter.append(Order.status == orderStatus.value)
        datas = Order.query.filter(and_(*dataFilter)).all()
        output =[]
        for data in datas:
            if data.active == 0:
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
        dataDict = {}
        if args['id']:
            datas = Order.query.filter(Order.id == args['id'])
        for data in datas:
            if data.active == 0:
                continue
            else:
                dataDict    = data.__dict__
                robotDict   = data.robot.__dict__
                missionDict = data.mission.__dict__
                
                dataDict.pop("_sa_instance_state")
                robotDict.pop("_sa_instance_state")
                missionDict.pop("_sa_instance_state")

                dataDict.pop("robot")
                dataDict.pop("mission")


                dataDict["robot"]  = robotDict
                dataDict["mission"] = missionDict
        return dataDict



  
class SetActivation(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('active')

        args = parser.parse_args()

        if  args['id']:
            data = Order.query.get(args['id']) 
            if args['active']:
                if args['active'] == "true":
                    data.active = 1
                    db.session.add(data)
                    db.session.commit()
                    return "True"
                if args['active'] == "false":
                    data.active = 0
                    db.session.add(data)
                    db.session.commit()
                    return "False"
     