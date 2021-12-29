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
        missions = Mission.query.all()

        for mission in missions:
            logging.info(mission)
            logging.warning(mission.steps)
            for step in mission.steps:
                logging.error(step.products)