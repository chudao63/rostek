import logging
import re
from flask_restful import Resource, reqparse
from flask_sqlalchemy.model import camel_to_snake_case
from humanfriendly.terminal import output
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.sqltypes import REAL
from app.models.step import Step
from utils.apimodel import BaseApiPagination
from app.models.mission import Mission

class MissionApi(BaseApiPagination):
    """
    URL: /location
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Mission, "/mission")


class MissionDetailApi(Resource):
    """
    URL: /
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
 
        output = []
        if args['id']:
            datas = Mission.query.filter(Mission.id == args['id'])
        for data in datas:
            dataDict    = data.__dict__
            stepDict = data.step
            dataDict.pop("_sa_instance_state")
            # output.append(stepDict)
            logging.warning(stepDict)

            dataDict["steps"] = output
        # return dataDict
 

class MissionStepApi(Resource):
    def get(self):
        parser   = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        if args['id']:
            missions = Mission.query.filter(Mission.id == args['id'])

        for mission in missions:
            listSteps   = []
            for x in range(len(mission.steps)):
                missionStepDict = mission.steps[x].__dict__
                missionStepDict.pop("_sa_instance_state")
                missionStepDict.pop("missions")
                listSteps.append(missionStepDict)
                
            missionDict = mission.__dict__
            missionDict.pop("_sa_instance_state")
            missionDict["steps"] = listSteps
            return missionDict

   

