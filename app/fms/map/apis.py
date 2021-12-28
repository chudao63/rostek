import logging
import re
from sqlalchemy.sql.expression import outerjoin

from sqlalchemy.sql.sqltypes import DateTime
from app.models.map import Map
from app.models.position import Position
from utils.apimodel import BaseApiPagination, ApiBase, ApiCommon
from flask_restful import Api, Resource, reqparse, request
import os, sys
from flask import send_from_directory
from app.models.map import Map, MapData
from app import APP_PATH, db
# from app.ros.subcriber import Monitor
from utils.common import object_as_dict, create_response_message
import yaml
from utils.yamlmodel import YamlReadWrite

class MapApiBase(BaseApiPagination):
    """
    URL: /map
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Map, "/map")

class UploadMapApi(ApiBase):
	@ApiBase.exception_error
	def post(self):
		"""
		Thêm ảnh lên sever, tên ảnh lấy theo Id trên db
		URL: '/upload'
		"""
		map = Map()
		db.session.add(map)
		db.session.commit()
	
		if request.files:
			infile = request.files['file']
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/img/{map.id}.png"

		infile.save(fileName)
		return create_response_message("Thêm mới thành công", 200)

class DisplayMapApi(Resource):
    """
    Lấy dữ liệu bản đồ theo tên
    URL: '/display'
    Param: 'imageName'
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imageName')
        args = parser.parse_args()
        return send_from_directory(
            directory= f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/app/fms/map/img", filename= f"{args['imageName']}.png")

class DeleteImageApi(ApiBase):

	@ApiBase.exception_error
	def get(self):
		"""
		Xóa img trên sever theo id, đồng thời xóa trên db
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('id')
		args = parser.parse_args()

		if args['id']:
			deleteImage = Map.query.filter(Map.id == args['id']).one()
			db.session.delete(deleteImage)
			db.session.commit()
			return create_response_message("Xóa thành công", 200)
        
class ActiveMapDataApi(ApiBase):
	def patch(self):
		"""
		CHUYỂN ĐỎI DỮ LIỆU MAP ĐANG SỬ DỤNG
		URL: /map_data_active
		Body: Truyền Json
		"""
		parser = self.json_parser(["id"], [])
		if parser["validate"]:
			data_id = parser["data"]["id"]
			mapDataActive = MapData.query.filter(MapData.active == True).all()
			if mapDataActive:
				mapDataActive[0].active = False
				db.session.add(mapDataActive[0])
				db.session.commit()
			mapData = MapData.query.get(data_id)
			mapData.active = True
			db.session.add(mapData)
			db.session.commit()
			return create_response_message("Active thành công",200)
		return parser["message"]

class PointAPI(ApiBase):
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
		data = request.get_json(force=True)
		for dataIndex in data['points']:
			position = Position(X = dataIndex['x'], Y = dataIndex['y'], name = dataIndex['name'], action = dataIndex['type'])
			db.session.add(position)
			db.session.commit()
		return create_response_message("Thêm điểm thành công", 200)
		

class MapDataApi(ApiBase):
	@ApiBase.exception_error
	def get(self):
		"""
		Lấy danh sách các Mapdata
		URL: '/mapdata'
		Method: GET
		"""
		mapDatas =MapData.query.all()
		output = []
		for mapData in mapDatas:
			mapDataDict = mapData.as_dict
			mapDataDict['positions'] = []
			for position in mapData.positions:
				mapDataDict['positions'].append(position.id)
				# mapDataDict['positions'].append(position.id)

			output.append(mapDataDict)
		return output

	@ApiBase.exception_error
	def post(self):
		"""
		Thêm một MapData mới 
		URL: '/mapdata'
		Method: POST
		"""
		data = request.get_json(force=True)

		map = MapData()
		if data['description']:
			map = MapData(description = data['description'])
		db.session.add(map)
		db.session.commit()
		return create_response_message("Thêm mới thành công", 200)


	@ApiBase.exception_error
	def patch(self):
		"""
		Thêm các điểm mới hoặc sửa các điểm cũ của một Map data
		URL:'/mapdata'
		Method: PATCH
		"""
		data = request.get_json(force = True)
		logging.warning(type(data['id']))
		mapData = MapData.query.get(data['id'])
		assert mapData is not None, f"MapData {data['id']} không tồn tại"
		for dataIndex in data:
			if dataIndex == 'description':
				mapData.description = data['description']
				db.session.add(mapData)
				db.session.commit()
			if dataIndex == 'positions':
				logging.warning(data['positions'])
			# cần xem lại
					






# class MapFileImEx(ApiBase):
# 	"""
#     URL: /map_data/file
# 	IMPORT EXPORT FILE YAML
# 	"""
# 	@ApiBase.exception_error
# 	def get(self):
# 		parser = reqparse.RequestParser()
# 		parser.add_argument("id", required = True)
# 		data = parser.parse_args()
# 		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
# 		fileName = f"{appPath}/app/fms/map/data/{data['id']}.yaml"
# 		yamlRead = YamlReadWrite.read(fileName)
# 		return yamlRead

# 	@ApiBase.exception_error
# 	def post(self):
# 		infile 	= request.files['file']
# 		id 		= request.form['id']
# 		assert infile, "File not found"
# 		MapData.import_file(infile,id)
# 		return create_response_message("Upload thành công", 200)


# class MapDataApi(ApiCommon):
# 	"""
#     URL: /map_data
# 	THÊM/XÓA/SỬA MAPDATA CHUNG
# 	"""
# 	def __init__(self):
# 		ApiCommon.__init__(self, MapData, "/map_data")
	
# 	@ApiBase.exception_error
# 	def get(self):
# 		mapDatas = MapData.query.all()
# 		return object_as_dict(mapDatas) 
	
# 	@ApiBase.exception_error
# 	def post(self):
# 		"""
# 			POST: Required ID in data
# 		"""
# 		parser = self.json_parser(["description"], [])
# 		if parser["validate"]:
# 			description = parser["data"]["description"]
# 			mapData = MapData( description = description)
# 			db.session.add(mapData)
# 			db.session.commit()
# 			MapData.create_data_file(mapData.id)
# 			return create_response_message("Thêm mới thành công", 200)
# 		return parser["message"]

# 	@ApiBase.exception_error
# 	def patch(self):
# 		"""
# 			PATCH: Required ID in data
# 		"""
# 		parser = self.json_parser(["id","active", "description"], ["id"])
# 		if parser["validate"]:
# 			mapData = MapData.query.get(parser["data"]["id"])
# 			assert mapData is not None, "Route không tồn tại"
# 			if "active" in parser["data"]:
# 				mapData.active = parser["data"]["active"]
# 			if "description" in parser["data"]:
# 				mapData.description = parser["data"]["description"]
# 			db.session.add(mapData)
# 			db.session.commit()
# 			return mapData.id
# 			# return create_response_message("Sửa thành công", 200)
# 		return parser["message"]

	# @ApiBase.exception_error
	# def delete(self):
	# 	"""
	# 		DELETE: Required ID or list ID in data
	# 	"""
	# 	args = ["id"]
	# 	required_args = []
	# 	parser = self.json_parser(args, required_args)
	# 	if parser["validate"]:
	# 		data = parser["data"]
	# 		if type(data["id"]) is list:
	# 			self.ModelType.delete_by_list_id(data["id"])
	# 			for id in data["id"]:
	# 				Route.delete_route_file(id)
	# 			return create_response_message("Xóa thành công", 200)
	# 		else:
	# 			self.ModelType.delete_by_id(data["id"])
	# 			Route.delete_route_file(id)
	# 			return create_response_message("Xóa thành công", 200)

class MapApi(ApiBase):
	"""URL: /route/detail
	DỮ LIỆU ĐƯỜNG ĐI TRÊN BẢN ĐỒ
	"""
	@ApiBase.exception_error
	def get(self):
		return MapData.get_data()
	
	@ApiBase.exception_error
	def post(self):
		"""
		Lưu dữ liệu vào trong bảng position trên db đồng thời lưu vào file yaml 
		"""
		data = request.get_json(force=True)

		for dataIndex in data['points']:
			position = Position(X = dataIndex['x'], Y = dataIndex['y'], name = dataIndex['name'], action = dataIndex['type'])
			db.session.add(position)
			db.session.commit()

		return create_response_message("Thêm điểm thành công", 200)













# class MapSpeedApi(ApiBase):
# 	"""
# 	TỐC ĐỘ CHẠY TRÊN BẢN ĐỒ
# 	"""
# 	def get(self):
# 		""" URL: /map_data/speed
# 		"""
# 		return Speed.get_configure()

# 	@ApiBase.exception_error
# 	def post(self):
# 		""" URL: /map_data/speed
# 		"""
# 		data = request.get_json(force=True)
# 		Speed.save_configure(data)
# 		Monitor.getInstance().reload_speed()
# 		return create_response_message("Lưu thành công", 200)


# Đã xong
# class MapImageApi(ApiBase):
# 	def get(self):
# 		""" URL: /map/img
# 		LẤY DỮ LIỆU HÌNH ẢNH BẢN ĐỒ TRANG CHỦ
# 		"""
# 		return send_from_directory(directory="map/img",filename="map.png" )

# 	@ApiBase.exception_error
# 	def post(self):
# 		infile 		= request.files['file']
# 		number 		= request.form['number']
# 		code 		= request.form['code']
# 		if code == generate_code(number):
# 			MapData.upload_image(infile)
# 			return create_response_message("Upload thành công", 200)
# 		else:
# 			return create_response_message("Hãy liên hệ nhà cung cấp để lấy mã", 409)