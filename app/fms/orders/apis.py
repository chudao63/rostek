import logging
from utils.apimodel import ApiBase, BaseApiPagination
from flask_restful import request
from app.models.orders import Order
from app import db
from utils.common import create_response_message
from utils.scheduling import Actions
from utils.vntime import *
from app import redisClient
# from app.ros.realtime import RobotRuning

class OrderApiBase(BaseApiPagination):
    """
    URL: /order-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order-base")

def send_order_id(orderId):
    extOrder = redisClient.lrange("orderList",0,-1)
    extOrder.append(orderId) 
    redisClient.lpush("orderList",*extOrder)

def printmessage():
    print("hello")

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
        Thêm một order mới, khi đến thời gian start_time của order sẽ gửi một order_id của order vừa tạo xuống redis
        URL: '/order'
        Method: POST
        """
        data = request.get_json(force = True)
        order = Order(start_time = data['start_time'], end_time = data['end_time'], robot_id = data['robot_id'], mission_id = data['mission_id'])
        db.session.add(order)
        db.session.commit()
        timeString = VnTimestamp.get_time_str(data['start_time'])
        logging.warning(order.id)

        Actions.get_instance().add_action({
            order.id : {
                "time" : timeString,
                "func" : send_order_id(order.id)
            }
        })
        logging.warning(timeString)
        return create_response_message(f"Thêm mới thành công", 200)

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
    # def get(self):
    #     """
    #     Khi nhấn Run Now của Order đang ở trạng thái Waitting thì sẽ gửi Order_id vào Key "robot{id}/command" của Server Redis
    #     """
    #     data = request.get_json(force = True) 
    #     order = Order.query.get(data['id'])
    #     redisClient.rpush(f"robot{order.robot_id}/command", f"{data['id']}")
    #     return create_response_message("Gửi lệnh thành công", 200)

    def post(self):
        """
        Khi nhấn Run Now của Order đang ở trạng thái Waitting thì sẽ gửi Order_id vào Key của Server Redis
        """
        data = request.get_json(force = True) 
        extOrder = redisClient.lrange("orderList",0,-1)
        if data['order'] in extOrder:
            return create_response_message("Invalid",409)
        else:
            extOrder.append(data['order']) 
            redisClient.lpush("orderList",*extOrder)
            return create_response_message("Gửi thành công",200)

