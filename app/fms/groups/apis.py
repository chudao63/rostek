import logging
import re
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse,request
from app.models.group import Group
from app import db
from app.ros.subcriber import Monitor
class GroupApi(BaseApiPagination):
    """
    URL: /order
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Group, "/group")
    def get(self):
        return BaseApiPagination.get(self)
class DeactiveGroupApi(Resource):
    def patch(self):
        data = request.get_json(force = True)
        group = Group.query.get(data["id"])
        group.active = data["active"]
        db.session.add(group)
        db.session.commit()
        return "patch done!"