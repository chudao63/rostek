from flask_restful import Resource, request
from app.models.area import *

class AreaApi(Resource):
    def get(self):
        datas = Area.query.all()
        output = []
        for data in datas:
            dataDict = data.__dict__
            dataDict.pop("_sa_instance_state")
            output.append(dataDict)

        return output