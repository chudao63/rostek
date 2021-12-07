
from flask_restful import Resource
from sqlalchemy.sql.sqltypes import REAL
from app.models.robot import Robot
from utils.apimodel import BaseApiPagination


class RobotApi(BaseApiPagination):

    def __init__(self):
        BaseApiPagination.__init__(self, Robot, "/robot")


class RobotFoundApi(Resource):
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
        