from logging import log
import logging
import re
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination, ApiBase
from flask_restful import Resource, reqparse,request
from app.models.group import Group
from app.models.robot import Robot

from app import db
from utils.common import create_response_message


class GroupApiBase(BaseApiPagination):
    """
    URL: /group-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Group, "/group-base")
class GroupApi(ApiBase):
    """
    URL: /group
    """

    @ApiBase.exception_error
    def get(self):
        groups = Group.query.all()
        output = []
        for group in groups:
            logging.warning(group.robots)
            if group.active == '0':
                continue
            else:
                groupDict = group.as_dict
                output.append(groupDict)
        return output

    @ApiBase.exception_error
    def post(self):
        data = request.get_json(force = True)
        groupDb = Group.query.all()
        for groupName in groupDb:
            if groupName.name == data['name']:
                return create_response_message(f"Tên {data['name']} đã tồn tại", 409)
                
        if 'mission_id' in data:
            group = Group(name = data['name'], mission_id = data['mission_id'])
            db.session.add(group)
        else: 
            group = Group(name = data['name'])
            db.session.add(group)
        db.session.commit()

        for robotId in data['robots']:
            robot = Robot.query.get(robotId)
            assert robot is not None, f"Robot {robotId} không tồn tại"
            robot.group_id = group.id 
            db.session.add(robot)
            db.session.commit()
        return create_response_message("Thêm mới thành công", 200)

    @ApiBase.exception_error
    def delete(self):
        data = request.get_json(force = True)
        group = Group.query.get(data["id"])
        group.active = data["active"]
        db.session.add(group)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)