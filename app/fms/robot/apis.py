from logging import log
import logging
from flask_restful import Api, Resource, reqparse, request
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.sql.base import NO_ARG
from sqlalchemy.util.langhelpers import group_expirable_memoized_property
from app.models.area import Area
from app.models.group import Group
from app.models.robot import Robot
from app.models.robot_status import RobotStatus
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
        Thêm robot mới
        URL: '/robot'
        Method: POST
        """
        data = request.get_json(force = True)
        robots = Robot.query.all()
        for robot in robots:
            if robot.name  == data['name'] and robot.active == 0:
                robot.name = data['name']
                robot.ip = data['ip']
                robot.port = data['port']
                robot.area_id = data['area_id']
                robot.type_id = data['type_id']
                robot.active = 1
                robot.group_id = data['group_id']
                db.session.add(robot)
                db.session.commit()
                return create_response_message("Thêm mới thành công", 200)
            if robot.name  == data['name']:
                return create_response_message(f"Tên {data['name']} đã tồn tại", 200)
            if robot.ip == data['ip']:
                return create_response_message(f"ip {data['ip']} đã tồn tại", 200)
        robot = Robot(name = data['name'], ip = data['ip'], port = data['port'], area_id = data['area_id'], type_id = data['type_id'],group_id = data['group_id'])
        db.session.add(robot)
        db.session.commit()
        return create_response_message("Thêm mới thành công", 200)



    @ApiBase.exception_error
    def patch(self):
        """
        Sửa thông tin robot cũ
        URL: '/robot'
        Method: PATCH
        """
        data = request.get_json(force = True)
        robotDb = Robot.query.all()
        robot = Robot.query.get(data['id'])
        assert robot is not None, f"Robot id {data['id']} không hợp lệ"

        if 'name' in data:
            for robot in robotDb:
                if robot.name == data['name']:
                    return create_response_message(f"Robot {data['name']} đã tồn tại", 200)
            robot.name = data['name']
            db.session.add(robot)

        if 'ip' in data:
            for robot in robotDb:
                if robot.ip == data['ip']:
                    return create_response_message(f"IP {data['ip']} đã tồn tại", 200)
            robot.ip = data['ip']
            db.session.add(robot)

        if 'port' in data:
            robot.port = data['port']
            db.session.add(robot)

        if 'area_id' in data:
            areaDb = Area.query.get(data['area_id'])
            assert areaDb is not None, f"Area {data['area_id']} không hợp lệ"
            robot.area_id = data['area_id']
            db.session.add(robot)

        if 'group_id' in data:
            groupDb = Group.query.get(data['group_id'])
            assert groupDb is not None, f"Group {data['group_id']}không hợp lệ"
            robot.group_id = data['group_id']
            db.session.add(robot)
        db.session.commit()
        return create_response_message("Sửa thành công", 200)


class DeleteRobotApi(ApiBase):
    @ApiBase.exception_error    
    def delete(self):
<<<<<<< HEAD
        """
        Xóa robot
        URL:'/robot'
        METHOD: DELETE
        """
        data = request.get_json(force = True)
        robot = Robot.query.get(data['id'])
        assert robot is not None, f"robot {data['id']} không tồn tại"
        robot.active = 0
        db.session.add(robot)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)


=======
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
>>>>>>> parent of b89d34c... Update Modles Robot
