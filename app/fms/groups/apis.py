import re
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination, ApiBase
from flask_restful import Resource, reqparse,request
from app.models.group import Group
from app import db
from utils.common import create_response_message


class GroupApiBase(BaseApiPagination):
    """
    URL: /group-base
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Group, "/group-base")
class GroupApi(ApiBase):
    """
    URL: /group
    """

    @ApiBase.exception_error
    def get(self):
        groups = Group.query.all()
        output = []
        for group in groups:
            if group.active == '0':
                continue
            else:
                groupDict = group.as_dict
                output.append(groupDict)
        return output


    @ApiBase.exception_error
    def delete(self):
        data = request.get_json(force = True)
        group = Group.query.get(data["id"])
        group.active = data["active"]
        db.session.add(group)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)