import logging

from humanfriendly.text import trim_empty_lines
from app.fms.orders.consts import ORDER_STATUS
from app.models.mission import Mission
from utils.apimodel import ApiBase, BaseApiPagination
from flask_restful import Api, Resource, reqparse,request
from app.models.orders import Order
from app import db
from sqlalchemy import and_
import os, sys
from utils.common import create_response_message


class OrderApiBase(BaseApiPagination):
    """
    URL: /order-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order-base")


class OrderApi(ApiBase):
    @ApiBase.exception_error
    def get(self):
        """
        Lấy order theo trạng thái
        URL: '/order'
        Method: GET
        """
        datas = Order.query.all()
        output =[]

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
                missionDict.pop("steps")


                dataDict.pop("robot")
                dataDict.pop("mission")


                dataDict["robot"]  = robotDict
                dataDict["mission"] = missionDict
                output.append(dataDict)
        return output

    @ApiBase.exception_error
    def post(self):
        """
        Thêm một order mới
        URL: '/order'
        Method: POST
        """
        data = request.get_json(force = True)
        order = Order(start_time = data['start_time'], end_time = data['end_time'], robot_id = data['robot_id'], mission_id = data['mission_id'])
        db.session.add(order)
        db.session.commit()
        return create_response_message("Thêm mới thành công", 200)

    @ApiBase.exception_error
    def delete(self):
        data = request.get_json(force = True)
        order = Order.query.get(data['id'])
        order.active = 0
        db.session.add(order)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)

class OrderDetailApi(ApiBase):
    @ApiBase.exception_error
    def get(self):
        """
        Xem chi tiết 1 Order
        URL: '/order-detail'
        """
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
