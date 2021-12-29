from logging import log
import logging
from flask_restful import Resource, reqparse, request
from app.models.robot import Robot
from utils.apimodel import BaseApiPagination
from app import db
from utils.apimodel import BaseApiPagination, ApiBase
from utils.common import create_response_message


class RobotBaseApi(BaseApiPagination):

    def __init__(self):
        BaseApiPagination.__init__(self, Robot, "/robot-base")



class RobotApi(Resource):
    def get(self):
        robotFounds = Robot.query.all()
        output = []

        for robotFound in robotFounds:
            if robotFound.active != "1":
                continue
            else:
                robotFoundDict = robotFound.__dict__
                robotFoundDict.pop("_sa_instance_state")
                output.append(robotFoundDict)
        return output

    @ApiBase.exception_error
    def post(self):
        data = request.get_json(force = True)
        logging.warning(data)
        for dataIndex in data:
            pass
            # assert "name" not in  data, "Không có 'name'"
            # logging.warning(dataIndex)


    @ApiBase.exception_error
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('active')
        args = parser.parse_args()

        if  args['id']:
            data = Robot.query.get(args['id']) 
            if args['active']:
                if args['active'] == '1':
                    data.active = 1
                    db.session.add(data)
                    db.session.commit()
                    return "Active robot"
            data.active = 0
            db.session.add(data)
            db.session.commit()
            return create_response_message("Xóa thành công", 200)

 