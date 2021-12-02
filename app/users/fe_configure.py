
from humanfriendly.terminal import message, warning
from .consts import *
from .models import *
from .validators import UserValidate
from app.ultils import *
from app.common.apimodel import ApiBase, BaseConfigureApi
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from passlib.hash import pbkdf2_sha256 as sha256
import logging
from sqlalchemy import exc, and_, func
import json
from .consts import *
import os, sys, yaml
from app.common.yamlmodel import YamlReadWrite
from pathlib import Path

class UserColumnApi(ApiBase):
    """URL: /user/column

    """
    # co token
    @jwt_required()
    def get(self):
        """
        Chứa thông tin tất cả các cột của bảng:
            - key: Dùng để hỉen thị tiêu đề + lúc edit + lúc thêm mới
        """
        allAtr = User.get_all_attr()
        currentUsername = get_jwt_identity()
        thisCol = UserTableColumn.query.filter(UserTableColumn.table == "user",UserTableColumn.username == currentUsername ).first()
        tableDatas = TABLE_JSON
        if not thisCol:
            userTableColumn = UserTableColumn(username = currentUsername, table = "user", data = json.dumps(tableDatas))
            db.session.add(userTableColumn)
            db.session.commit()
            return json.loads(userTableColumn.data)
        return json.loads(thisCol.data)

    @jwt_required()
    def patch(self):
        """
            Chỉnh sửa column nào được hiển thị trong table
        """
        allAtr = User.get_all_attr()
        parser = self.json_parser([], [])
        currentUsername = get_jwt_identity()
        thisCol = UserTableColumn.query.filter(UserTableColumn.table == "user",UserTableColumn.username == currentUsername ).first()
        tableData = []
        if not thisCol:
            userTableColumn = UserTableColumn(username = currentUsername, table = "user", data = json.dumps(parser['data']))
            db.session.add(userTableColumn)
            db.session.commit() 
            return "Chỉnh sửa thành công", 200
        thisCol.data = json.dumps(parser['data'])
        db.session.add(thisCol)
        db.session.commit()
        return "Chỉnh sửa thành công", 200
        
class UserFilterApi(BaseConfigureApi, YamlReadWrite):
    """URL: /user/filter
        Lấy giá trị filter trả về fontend
    """
    def __init__(self):
        self.init_base_path(str(os.path.dirname(__file__)))