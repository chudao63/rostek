from logging import log
import logging
import re
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.sqltypes import REAL
from app.models.mission import Mission
from utils.apimodel import ApiBase, BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.step import Step
from utils.common import create_response_message
from app import db
from app.models.position import Position
from app.models.mission import Mission
from sqlalchemy.sql.elements import or_



class StepApiBase(BaseApiPagination):
    """
    URL: /step-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Step, "/step-base")

class StepApi(ApiBase):
    def get(self):
        missions = Mission.query.all()
        for mission in missions:
            logging.info(mission)
            logging.warning(mission.steps)
            for step in mission.steps:
                logging.error(step.products)

    @ApiBase.exception_error
    def delete(self):
        """
        Xóa một step
        """
        data = request.get_json(force = True)
        missions = Mission.query.all()
        for mission in missions:
            for index in mission.steps:
                if index.id == data['id']:
                    while len(mission.steps):
                        mission.steps.pop(0)
                        db.session.add(mission)
                        db.session.commit()
        stepId = Step.query.get(data['id'])
        db.session.delete(stepId)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)