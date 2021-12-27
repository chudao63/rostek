import logging
from os import name
import re
from flask_restful import Resource, reqparse, request
from sqlalchemy.orm.util import outerjoin
from utils.apimodel import BaseApiPagination, ApiBase
from app.models.mission import Mission
from app.models.step import Step
from app.models.product import Product

from app import db
from utils.common import create_response_message
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
       
        missions = Mission.query.all()
        output = []
        for mission in missions:
            missionDict = mission.as_dict
            missionDict["steps"] = []
            for step in mission.steps:
                stepDict = step.as_dict
                for product in step.products:
                    stepDict["product"] = product.as_dict
                missionDict["steps"].append(stepDict)
            output.append(missionDict)
        return output
        # ---- Code cũ đúng nhưng dài ---- 
        # listSteps   = []
        # for indexStep in range(len(mission.steps)):
        #     listProduct = {}
        #     for indexProduct in range(len(mission.steps[indexStep].products)):
        #         productDict = mission.steps[indexStep].products[indexProduct].__dict__
        #         listProduct['id'] = productDict['id']
        #         listProduct['name'] = productDict['name']

        #     missionStepDict = mission.steps[indexStep].__dict__
        #     missionStepDict.pop("_sa_instance_state")
        #     missionStepDict.pop("missions")
        #     missionStepDict.pop("products")
        #     missionStepDict['products'] = listProduct
        #     listSteps.append(missionStepDict)
            
        # missionDict = mission.__dict__
        # missionDict.pop("_sa_instance_state")
        # missionDict["steps"] = listSteps
        # return missionDict



class CreateMissionApi(ApiBase):
    @ApiBase.exception_error
    def post(self):
        """
        URL: '/create-mision'
        Tạo mission mới 
        1, Ghi bản tin vào mission
        2, Ghi bản tin vào bảng Step
        3, Ghi bản tin vào bảng tạm giữa step và Product
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

            step = Step(start_point = stepIndex['start_point'], end_point = stepIndex['end_point'])
            db.session.add(step)
            db.session.commit()

            stepMission = Step.query.order_by(Step.id.desc()).first()
            product = Product.query.get(stepIndex['product'])
            stepMission.products.append(product)
    
            dataMission.steps.append(stepMission)
            db.session.add(dataMission)
            db.session.commit()
        return create_response_message("Tạo mới thành công", 200)

        #Body:
        #     {
        # "name" : "MissionTest5",
        # "step" : [
        #             {
        #                 "start_point" : 2,
        #                 "end_point"   : 1,
        #                 "product"     : 1
        #             },
        #             {
        #                 "start_point" : 1,
        #                 "end_point"   : 2,
        #                 "product"     : 2
        #             }
        #         ]
        #    }   
    @ApiBase.exception_error
    def patch(self):
        """
        Hàm sửa edit mission

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
                    # assert "id" not in stepIndex,"Thiếu id trong step"

                    step = Step.query.get(stepIndex['id'])
                    step.start_point = stepIndex['start_point']
                    step.end_point = stepIndex['end_point']

                    while len(step.products): # xoa het cac product trong step
                        step.products.pop(0)
                    # them moi product
                    productId = stepIndex["products"]["id"]
                    productDb = Product.query.get(productId)
                    assert productDb is not None, f"Product {productId} khong ton tai"
                    step.products.append(productDb)
                    db.session.add(step)
                    db.session.commit()
                
        return create_response_message("Sửa thành công", 200)
        # Body:
        #     {
        #         "id" : 1,
        #         "name" : "Mission - 1 - patch",
        #         "steps" : [
        #             {
        #                 "id" : 1,
        #                 "start_point" : 2,
        #                 "end_point"   : 2,
        #                 "products"     : {
        #                     "id" : 2
        #                 }
        #             },
        #             {   
        #                 "id" : 2,
        #                 "start_point" : 1,
        #                 "end_point"   : 1,
        #                 "products"     : {
        #                     "id" :1
        #                 }
        #             }
        #         ]
        #     }