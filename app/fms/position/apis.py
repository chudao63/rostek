import logging

from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.sqltypes import NullType
from utils.apimodel import BaseApiPagination, ApiBase
from app.models.position import Position
from app.models.mission import Mission
from app.models.step import Step
from flask_restful import Resource, reqparse, request
from sqlalchemy.sql.expression import and_, null, or_

from utils.common import create_response_message
from app import db

class PositionApi(BaseApiPagination):
    """
    URL: /position
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Position, "/position")

class PointApi(ApiBase):
    @ApiBase.exception_error
    def get(self):
        """
        Trả về tất cả các điểm đã được lưu trên db
        URL: '/point'
        method: GET
        """
        positions = Position.query.all()

        output = []
        for position in positions:
            positionDict = position.as_dict
            output.append(positionDict)
        return output
        
    @ApiBase.exception_error
    def post(self):
        """
        Thêm danh sách các điểm mới 
        URL: '/point'
        method: POST
        Body:
            {
                "description": "null",
                "points":
                [
                    {
                        "name": "Point44",
                        "x": 236,
                        "y": 277,
                        "type": "MOVING"
                    }
                ]
        """

        data =request.get_json(force = True)
        pointDbs = Position.query.all()

        for dataIndex in data['points']:
            if 'id' in dataIndex:
                point = Position.query.get(dataIndex['id'])
                point.x = dataIndex['x']
                point.y = dataIndex['y']
                point.name = dataIndex['name']
                point.type = dataIndex['type']
                point.map_data_id = dataIndex['map_data_id']
                db.session.add(point)
                db.session.commit()
            else:
                for pointDb in pointDbs:
                    if pointDb.name == dataIndex['name']:
                        return create_response_message(f"Tên {dataIndex['name']} đã tồn tại", 409)
                position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
                db.session.add(position)
                db.session.commit()
        return create_response_message("Sửa map_data thành công", 200)

    
    @ApiBase.exception_error
    def delete(self):
        """
        Xóa một điểm
        Khi xóa một điểm ->  Xóa step chứa điểm đó -> Xóa các bước của mission chứa step đó
        URL:'/point'
        METHOD: DELETE
        """
        data = request.get_json(force = True)
        position = Position.query.get(data['id'])
        assert position is not None, f"Point {data['id']} không tồn tại"
        steps = Step.query.filter(or_((Step.start_point == data['id']), (Step.end_point == data['id']))).all()

        for step in steps:
            if step.start_point == data['id']:
                step.start_point = None
                db.session.add(step)
            if step.end_point == data['id']:
                step.end_point = None
                db.session.add(step)
            db.session.commit()
        db.session.delete(position)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)



    