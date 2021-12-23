from logging import log
import logging
import re
from sqlalchemy.sql.sqltypes import REAL
from app.models.mission import Mission
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.step import Step

class StepApi(BaseApiPagination):
    """
    URL: /step
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Step, "/step")

class StepProductApi(Resource):
    def get(self):
        steps = Step.query.all()
        missions = Mission.query.all()

        for mission in missions:
            logging.info(mission)
            logging.warning(mission.steps)
            for step in mission.steps:
                logging.error(step.products)

        # output = []
        # for step in steps:
        #     logging.warning(step.products)
        #     logging.warning(step.missions)
        #     # stepDict = step.__dict__
        #     # stepDict.pop("_sa_instance_state")
        #     # stepDict.pop("products")
        #     # stepDict.pop("missions")
        #     # output.append(stepDict)
        #     # logging.warning(output)
        # return output