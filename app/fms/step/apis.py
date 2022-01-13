from logging import log
import logging
import re
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.sqltypes import REAL
from app.models.mission import Mission
from utils.apimodel import ApiBase, BaseApiPagination
from flask_restful import Api, Resource, reqparse,request
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
        """
        Lấy dữ liệu các step lưu trên database
        URL: /step
        Method: GET
        """
        missions = Mission.query.all()
        for mission in missions:
            logging.info(mission)
            logging.warning(mission.steps)
            for step in mission.steps:
                logging.error(step.products)


    @ApiBase.exception_error
    def post(self):
        """
        Thêm một step mới
        URL: /step
        Method: POST
        """
        data = request.get_json(force = True)
        points = Position.query.all()
        notiStartPoint = 0
        notiEndPoint = 0
        assert "start_point" in data, "Thiếu start_point"
        assert "end_point" in data, "Thiếu end_point"
        assert "action_start_point" in data, "Thiếu action_start_point"
        assert "action_end_point" in data, "Thiếu action_end_point"


        for point in points:
            if point.id == data['start_point']:
                notiStartPoint = 1
            if point.id == data['end_point']:    
                notiEndPoint = 1



        if notiStartPoint == 1 and notiEndPoint == 1:
            stepPoint = Step(start_point = data['start_point'], end_point = data['end_point'], action_start_point = data['action_start_point'], action_end_point = data['action_end_point'])
            
            db.session.add(stepPoint)
            db.session.commit()
            return create_response_message("Thêm thành công", 200)
        elif notiEndPoint == 0:
            return create_response_message(f"Point {data['end_point']} không hợp lệ",409)
        elif notiStartPoint == 0:
            return create_response_message(f"Point {data['start_point']} không hợp lệ",409)



    @ApiBase.exception_error
    def delete(self):
        """
        Xóa một step
        URL: /step
        Method: DELETE
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