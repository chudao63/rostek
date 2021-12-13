import logging
from app.fms.orders.consts import ORDER_STATUS
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.orders import Order
from app import db
from sqlalchemy import and_
import os, sys

class OrderApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Order, "/order")


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
            # robotName = data.robot.name
            robotName = data.robot.name
            missionName = data.mission.name
            job_type = data.mission.type_job
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
                dataDict['job_type'] = job_type
                
                output.append(dataDict)
        return output

class OrderDetailsApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

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

class UpdateOrderApi(Resource):
    def patch(self):
        data = request.get_json(force=True)
        robot = Order.query.get(data['id'])
        

     
class Test(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileName')

        args = parser.parse_args()

        if request.files:
            infile = request.files['file']
            appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
            fileName = f"{appPath}/upload_file/{str(args['fileName'])}.png"
            infile.save(fileName)
            return "Done!!!"
