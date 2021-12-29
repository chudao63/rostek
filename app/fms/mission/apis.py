import logging
from os import name
import re
from flask_restful import Resource, reqparse, request
from humanfriendly.terminal import auto_encode
from sqlalchemy.orm.util import outerjoin
from utils.apimodel import BaseApiPagination, ApiBase
from app.models.mission import Mission
from app.models.step import Step
from app.models.product import Product
from app.models.position import Position

from app import db
from utils.common import create_response_message
class MissionBaseApi(BaseApiPagination):
    """
    URL: /mission-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Mission, "/mission-base")



def edit_step_data(data):
    """
    Sửa các step có trong 1 Mission
    data: dữ liệu json truyền vào
    """
    for stepIndex in data['steps']:
        if "id" in stepIndex:
            startPointId = stepIndex['start_point_id']
            startPointDb = Position.query.get(startPointId)

            assert startPointDb is not None, f"Point {startPointId} không tồn tại"
            endPointId = stepIndex['end_point_id']
            endPointDb = Position.query.get(endPointId)

            assert endPointDb is not None, f"Point {endPointId} không tồn tại"
            step = Step.query.get(stepIndex['id'])
            assert step is not None, f"Step {stepIndex['id']} không tồn tại"

            step.start_point = stepIndex['start_point_id']
            step.end_point = stepIndex['end_point_id']
            while len(step.products): # xoa het cac product trong step
                step.products.pop(0)
            # them moi product

            productId = stepIndex["product_id"]
            productDb = Product.query.get(productId)
            assert productDb is not None, f"Product {productId} không tồn tại"

            step.products.append(productDb)
            db.session.add(step)
            db.session.commit()

def new_step_data(missionDb, start_point, end_point, productData):
    """
    Ghi thêm một step mới vào Mission cũ
    missionDb  : Mission muốn sửa
    start_point: Điểm bắt đầu của step
    end_point  : Điểm kết thúc của step
    productData: Hàng hóa phục vụ cho step
    """
    step = Step(start_point = start_point, end_point = end_point)
    db.session.add(step)
    db.session.commit()
    stepMission = Step.query.order_by(Step.id.desc()).first()
    product = Product.query.get(productData)
    stepMission.products.append(product)

    missionDb.steps.append(stepMission)
    db.session.add(missionDb)
    db.session.commit()



class MissionApi(Resource):
    def get(self):
        """
        Lấy dữ liệu các Mission có trong database
        """
        missions = Mission.query.all()
        output = []
        for mission in missions:
            missionDict = mission.as_dict
            missionDict["steps"] = []
            
            for step in mission.steps:
                stepDict = step.as_dict
                startPointDict = {}
                endPointDict = {}
                startPoint = Position.query.get(step.start_point)
                endPoint   = Position.query.get(step.end_point)

                startPointName = startPoint.name
                startPointId = startPoint.id

                endPointName  = endPoint.name
                endPointId  = endPoint.id

                startPointDict['id'] = startPointId
                startPointDict['name'] = startPointName

                endPointDict['id'] = endPointId
                endPointDict['name'] = endPointName
            
                stepDict['start_point'] = startPointDict
                stepDict['end_point'] = endPointDict
                for product in step.products:
                    stepDict["product"] = product.as_dict
                
                missionDict["steps"].append(stepDict)

            output.append(missionDict)
        return output

    @ApiBase.exception_error
    def post(self):
        """
        URL: '/create-mision'
        Tạo mission mới 
        1, Ghi bản tin vào mission
        2, Ghi bản tin vào bảng Step
        3, Ghi bản tin vào bảng tạm giữa step và Product
        Body:
            {
                "name" : "MissionTest5",
                "step" : [
                            {
                                "start_point_id" : 2,
                                "end_point_id"   : 1,
                                "product_id"     : 1
                            },
                            {
                                "start_point_id" : 1,
                                "end_point_id"   : 2,
                                "product_id"     : 2
                            }
                        ]
           }   
        """
        missionNames = Mission.query.all()
        data = request.get_json(force = True)
        for missionName in missionNames:
            if missionName.name == data['name']:
                return create_response_message("Tên đã tồn tại", 400)

        mission = Mission(name = data['name'])
        db.session.add(mission)
        db.session.commit()
        dataMission = Mission.query.order_by(Mission.id.desc()).first()

        for stepIndex in data['steps']:
            step = Step(start_point = stepIndex['start_point_id'], end_point = stepIndex['end_point_id'])
            db.session.add(step)
            db.session.commit()
            stepMission = Step.query.order_by(Step.id.desc()).first()
            product = Product.query.get(stepIndex['product_id'])
            stepMission.products.append(product)
    
            dataMission.steps.append(stepMission)
            db.session.add(dataMission)
            db.session.commit()
        return create_response_message("Tạo mới thành công", 200)

     
    @ApiBase.exception_error
    def patch(self):
        """
        Hàm sửa mission
        Body:
            {
                "id" : 1,
                "name" : "Mission - 1 - patch",
                "steps" : [
                    {
                        "id" : 1,
                        "start_point_id" : 2,
                        "end_point_id"   : 2,
                        "product_id"     : 1
                    },
                    {   
                        "id" : 2,
                        "start_point_id" : 1,
                        "end_point_id"   : 1,
                        "product_id"     : 1

                    }
                ]
            }
        """
        data = request.get_json(force = True)
        mission = Mission.query.get(data['id'])

        assert mission is not None, f"Mission {data['id']} không tồn tại"
        for dataIndex in data:
            if dataIndex == 'name':
                mission.name = data['name']
                db.session.add(mission)
                db.session.commit()
            if dataIndex == 'steps':                
                for stepIndex in data['steps']:
                    if "id" in stepIndex:
                        edit_step_data(data)
                    if "id" not in stepIndex:
                        new_step_data(mission, stepIndex['start_point_id'],stepIndex['end_point_id'],stepIndex['product_id'])
        return create_response_message("Sửa thành công", 200)
 