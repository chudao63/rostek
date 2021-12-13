from flask_restful import Resource, reqparse
from app.models.robot import Robot
from utils.apimodel import BaseApiPagination

from app import db

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
class DeleteRobotApi(Resource):
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

            return "Delete done"
