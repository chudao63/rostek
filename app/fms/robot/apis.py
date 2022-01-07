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
        Lấy dữ liệu tất cả robot trên database
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
        Thêm robot mới, nếu trùng tên với robot cũ đã xóa thì thay đổi thông tin robot cũ
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
                if 'group_id' in data:
                    robot.group_id = data['group_id']
                else:
                    robot.group_id = None
                db.session.add(robot)
                db.session.commit()
                return create_response_message("Thêm mới thành công", 200)
            if robot.name  == data['name']:
                return create_response_message(f"Tên {data['name']} đã tồn tại", 409)
            if robot.ip == data['ip']:
                return create_response_message(f"ip {data['ip']} đã tồn tại", 409)
        if 'group_id' in data:
            robot = Robot(name = data['name'], ip = data['ip'], port = data['port'], area_id = data['area_id'], type_id = data['type_id'],group_id = data['group_id'])
            db.session.add(robot)
            db.session.commit()
            return create_response_message("Thêm mới thành công", 200)
        robot = Robot(name = data['name'], ip = data['ip'], port = data['port'], area_id = data['area_id'], type_id = data['type_id'])
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
            for robotDetail in robotDb:
                if robotDetail.name == data['name'] and robotDetail.id != data['id']:
                    return create_response_message(f"Robot {data['name']} đã tồn tại", 409)
            robot.name = data['name']
            db.session.add(robot)
            db.session.commit()

        if 'ip' in data:
            for robotDetail in robotDb:
                if robotDetail.ip == data['ip'] and robotDetail.id != data['id']:
                    return create_response_message(f"IP {data['ip']} đã tồn tại", 409)
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


    @ApiBase.exception_error
    def delete(self):
        """
        Xóa robot
        URL:'/robot'
        METHOD: DELETE
        """
        data = request.get_json(force = True)
        robot = Robot.query.get(data['id'])
        assert robot is not None, f"robot {data['id']} không tồn tại"
        robot.group_id = None
        for order in robot.order:
            if order.status == 2:
                return create_response_message("Robot đang làm nhiệm vụ, không thể xóa", 409)
            if order.status == 1:
                order.robot_id = None
                db.session.add(order)
        robot.active = 0

        db.session.add(robot)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)


