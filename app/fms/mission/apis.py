import logging
from flask_restful import Resource, reqparse
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


   

