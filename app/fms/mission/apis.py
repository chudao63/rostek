import logging
from flask_restful import Resource, reqparse, request
from utils.apimodel import BaseApiPagination
from app.models.mission import Mission
from app.models.step import Step
from app.models.product import Product

from app import db
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
        parser.add_argument('id', required=True,help="id cannot be blank!")
        args = parser.parse_args()

        mission = Mission.query.get(args['id'])

        missionDict = mission.as_dict
        missionDict["steps"] = []
        for step in mission.steps:
            stepDict = step.as_dict
            for product in step.products:
                stepDict["product"] = product.as_dict
            missionDict["steps"].append(stepDict)
        return missionDict
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



class CreateMissionApi(Resource):
    def post(self):
        """
        URL: '/create-mision'
        Tạo mission mới 
        1, Ghi bản tin vào mission
        2, Ghi bản tin vào bảng Step
        3, Ghi bản tin vào bảng tạm giữa step và Product
        """
        data = request.get_json(force = True)
        mission = Mission(name = data['name'])
        db.session.add(mission)
        db.session.commit()
        dataMission = Mission.query.order_by(Mission.id.desc()).first()

        for stepIndex in data['step']:

            step = Step(start_point = stepIndex['start_point'], end_point = stepIndex['end_point'])
            db.session.add(step)
            db.session.commit()

            stepMission = Step.query.order_by(Step.id.desc()).first()
            product = Product.query.get(stepIndex['product'])
            stepMission.products.append(product)
    
            dataMission.steps.append(stepMission)
            db.session.add(dataMission)
            db.session.commit()

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