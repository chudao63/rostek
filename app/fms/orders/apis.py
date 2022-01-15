import logging

from humanfriendly.text import trim_empty_lines
from app.fms.orders.consts import ORDER_STATUS
from app.models.mission import Mission
from utils.apimodel import ApiBase, BaseApiPagination
from flask_restful import Api, Resource, reqparse,request
from app.models.orders import Order
from app import db
import os, sys
from utils.common import create_response_message
# from app.ros.subcriber import *
from app.models.robot import Robot
from app.models.position import Position

from app import redisClient
# from app.ros.realtime import RobotRuning

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
        Lấy tất cả các order đang active trên db
        URL: '/order'
        Method: GET
        """
        orders = Order.query.all()
        output =[]
        for data in orders:
            if data.active == 0:
                continue
            else:
                dataDict = data.as_dict
                if data.robot_id is not None:
                    if data.robot.active == True or data.status == 0:
                        robotDict   = data.robot.as_dict
                    else:
                        robotDict = None
                else:
                    robotDict = None
                if data.mission_id is not None:
                    if data.mission.active == True or data.status == 0:
                        missionDict = data.mission.as_dict
                    else:
                        missionDict = None
                else:
                    missionDict = None
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
        """
        Xóa Order 
        URL: /order
        Method: DELETE
        """
        data = request.get_json(force = True)
        order = Order.query.get(data['id'])
        order.active = 0
        db.session.add(order)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)


class RunNowOrder(ApiBase):
    def get(self):
        """
        Khi nhấn Run Now của Order đang ở trạng thái Waitting thì sẽ gửi Order_id vào Key "robot{id}/command" của Server Redis
        """
        data = request.get_json(force = True) 
        order = Order.query.get(data['id'])
        redisClient.rpush(f"robot{order.robot_id}/command", f"{data['id']}")
        return create_response_message("Gửi lệnh thành công", 200)