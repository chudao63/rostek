from logging import log
import logging
from flask_restful import Api, Resource, reqparse, request
from flask_sqlalchemy import get_debug_queries
from app.models.group import Group
from app.models.robot import Robot
from utils.apimodel import BaseApiPagination
from app import db
from utils.apimodel import BaseApiPagination, ApiBase
from utils.common import create_response_message


class RobotBaseApi(BaseApiPagination):

    def __init__(self):
        BaseApiPagination.__init__(self, Robot, "/robot-base")



class RobotApi(ApiBase):
    def get(self):
        """
        URL: '/robot'
        Method: GET
        """
        robotFounds = Robot.query.all()
        output = []
        for robotFound in robotFounds:
            if robotFound.active != 1:
                continue
            else:
                robotFoundDict = robotFound.__dict__
                robotFoundDict.pop("_sa_instance_state")
                output.append(robotFoundDict)
        return output

    @ApiBase.exception_error
    def post(self):
        """
        URL: '/robot'
        Method: POST
        """
        data = request.get_json(force = True)
        robot = Robot(name = data['name'], ip = data['ip'], port = data['port'], area_id = data['area_id'], type_id = data['type_id'],group_id = data['group_id'])
        db.session.add(robot)
        db.session.commit()
        return create_response_message("Thêm mới thành công", 200)


    @ApiBase.exception_error
    def patch(self):
        """
        URL: '/robot'
        Method: PATCH
        """
        data = request.get_json(force = True)
        robot = Robot.query.get(data['id'])
        robot = Robot(name = data['name'], ip = data['ip'], port = data['port'], area_id = data['area_id'], type_id = data['type_id'],group_id = data['group_id'])
        db.session.add(robot)
        db.session.commit()


class DeleteRobotApi(ApiBase):
    @ApiBase.exception_error    
    def delete(self):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        """
        Xóa robot
        URL:'/robot'
        METHOD: DELETE
        """
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
        data = request.get_json(force = True)
        robot = Robot.query.get(data['id'])
        assert robot is not None, f"robot {data['id']} không tồn tại"
        robot.active = 0
        db.session.add(robot)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)


=======
=======
>>>>>>> parent of b89d34c... Update Modles Robot
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
<<<<<<< HEAD
            return create_response_message("Xóa thành công", 200)
>>>>>>> parent of b89d34c... Update Modles Robot
=======
            return create_response_message("Xóa thành công", 200)
>>>>>>> parent of b89d34c... Update Modles Robot
