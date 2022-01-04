import logging
from app import db
from os import path
from utils.apimodel import BaseApiPagination
from app.models.position import Position
from app.models.map import MapData
from utils.common import create_response_message
from flask_restful import request

class PositionApi(BaseApiPagination):
    """
    URL: /position
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Position, "/position")

    # def post(self):
    #     args = self.ModelType.get_all_attr()
    #     # required_args = ["id"]
    #     required_args = []
    #     parser = self.json_parser(args, required_args)
    #     if parser["validate"]:
    #         data = parser["data"]
    #     self.ModelType.add_new_from_dict(data):
    #         return create_response_message("Thêm mới thành công", 200)
    #     return parser["message"]
    def patch(self):
        if "/edit" in request.path:
            args = []
            required_args = ["data"]
            parser = self.json_parser(args, required_args)
            if parser["validate"]:
                try: 
                    datas = parser["data"]["data"]
                    for data in datas:
                        if data["type_edit"] == "new":
                            # check dữ liệu truyền về
                            assert data["name"]  , f"Không có dữ liệu name "
                            assert data["x"]     , f"Không có dữ liệu x "
                            assert data["y"]     , f"Không có dữ liệu y "
                            assert data["R"]     , f"Không có dữ liệu R "
                            assert data["type"]  , f"Không có dữ liệu type "
                            assert data["map_data_id"], f"Không có dữ liệu map_data_id "
                            name = str(data["name"])
                            x = float(data["x"])
                            y = float(data["y"])
                            r = float(data["R"])
                            type = str(data["type"])
                            mapdata_id = int(data["map_data_id"])
                            # check có posistion này chưa
                            position = Position.query.filter(Position.name == data["name"]).first()
                            assert not position, f"Đã có position {data['name']}"
                            mapData = MapData.query.get(mapdata_id)
                            assert mapData, f"Không có map {mapdata_id}"
                            addPosition = Position(name = name, x = x, y = y, R = r, type = type, map_data_id = mapData.id)
                            db.session.add(addPosition)
                        if data["type_edit"] == "edit":
                            position_edit = Position.query.get(data["id"])
                            assert not position, f"Không có position id là {data['id']}"
                            if "name" in data:
                                position_edit.name = data["name"]
                            if "x" in data:
                                position_edit.x = data["x"]
                            if "y" in data:
                                position_edit.y = data["y"]
                            if "R" in data:
                                position_edit.R = data["R"]
                            if "type" in data:
                                position_edit.type = data["type"]
                            if "map_data_id" in data:
                                map_data = MapData.query.get(data["map_data_id"])
                                position_edit.map_data_id = map_data.id
                            db.session.add(position_edit)
                        if data["type_edit"] == "delete":
                            # xóa point data
                            pass
                        logging.warning(data)
                    # db.session.commit()
                except Exception as e:
                    msg = str(e)
                    logging.error(msg)
                    return create_response_message(msg, 422)
