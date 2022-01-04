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
            # robotName = data.robot.name
            robotName = data.robot.name
            missionName = data.mission.name
            logging.error(robotName)
            if data.active == 0:
                continue
            else:
                dataDict = data.__dict__
                dataDict.pop("_sa_instance_state")
                dataDict.pop("robot")
                dataDict.pop("mission")
                dataDict["robot_name"] = robotName
                dataDict["mission_name"] = missionName
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



  
class SetActivation(ApiBase):
    @ApiBase.exception_error
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
                    return create_response_message("Active thành công", 200)
                if args['active'] == "false":
                    data.active = 0
                    db.session.add(data)
                    db.session.commit()
                    return create_response_message("Xóa thành công", 200)

     
class Test(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileName')

        args = parser.parse_args()

        if request.files:
            infile = request.files['file']
            appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
            fileName = f"{appPath}/app/fms/map/img/{str(args['fileName'])}.png"
            infile.save(fileName)
            return "Done!!!"

