import logging
from app.models.map import Map
from utils.apimodel import BaseApiPagination, ApiBase, ApiCommon
from flask_restful import Resource, reqparse, request
import os, sys
from flask import send_from_directory
from app.models.map import Map, MapData
from app import db
from app.ros.subcriber import Monitor
from utils.common import object_as_dict, create_response_message


class MapApiBase(BaseApiPagination):
    """
    URL: /map
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Map, "/map")

class UploadMapApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imageName')

        args = parser.parse_args()

        # if args['imageName']:
        #     # datas = Map.query.all()
        #     # for data in datas:
        #     #     logging.error(data.file_name)
        #     #     if data.file_name == args['imageName']:
        #     #         return "Namesake"

        #     map = Map(file_name = args['imageName'])
        #     db.session.add(map)
        #     db.session.commit()
        

        if request.files:
            infile = request.files['file']
            appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
            fileName = f"{appPath}/app/fms/map/img/{str(args['imageName'])}.png"

            infile.save(fileName)
            return "Done!!!"

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
        logging.error(args)

        return send_from_directory(
            directory= f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/app/fms/map/img", filename= f"{args['imageName']}.png")

class DeleteImageApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        if args['id']:
            deleteImage = Map.query.filter(Map.id == args['id']).one()
            db.session.delete(deleteImage)
            db.session.commit()
            return "delete done"
        


class ActiveMapDataApi(ApiBase):
	def patch(self):
		"""
		CHUYỂN ĐỎI DỮ LIỆU MAP ĐANG SỬ DỤNG
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
			# Monitor.getInstance().reload_map_data()
			# return create_response_message("Thêm mới thành công", 200)
			return create_response_message("Active thành công",200)
		return parser["message"]


class MapFileImEx(ApiBase):
	"""
    URL: /map_data/file
	IMPORT EXPORT FILE YAML
	"""
	@ApiBase.exception_error
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("id", required = True)
		data = parser.parse_args()
		return send_from_directory(directory="fms/map/data",filename=f"{data['id']}.yaml" )
        

	@ApiBase.exception_error
	def post(self):
		infile 	= request.files['file']
		id 		= request.form['id']
		assert infile, "File not found"
		MapData.import_file(infile,id)
		Monitor.getInstance().reload_map_data()
		return create_response_message("Upload thành công", 200)


class MapDataApi(ApiCommon):
	"""
    URL: /map_data
	THÊM/XÓA/SỬA MAPDATA CHUNG
	"""
	def __init__(self):
		ApiCommon.__init__(self, MapData, "/map_data")
	
	@ApiBase.exception_error
	def get(self):
		mapDatas = MapData.query.all()
		return object_as_dict(mapDatas) 
	
	@ApiBase.exception_error
	def post(self):
		"""
			POST: Required ID in data
		"""
		parser = self.json_parser(["description"], [])
		if parser["validate"]:
			description = parser["data"]["description"]
			mapData = MapData( description = description)
			db.session.add(mapData)
			db.session.commit()
			MapData.create_data_file(mapData.id)
			return create_response_message("Thêm mới thành công", 200)
		return parser["message"]

	@ApiBase.exception_error
	def patch(self):
		"""
			PATCH: Required ID in data
		"""
		parser = self.json_parser(["id","active", "description"], ["id"])
		if parser["validate"]:
			mapData = MapData.query.get(parser["data"]["id"])
			assert mapData is not None, "Route không tồn tại"
			if "active" in parser["data"]:
				mapData.active = parser["data"]["active"]
			if "description" in parser["data"]:
				mapData.description = parser["data"]["description"]
			db.session.add(mapData)
			db.session.commit()
			return mapData.id
			# return create_response_message("Sửa thành công", 200)
		return parser["message"]

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
		data = request.get_json(force=True)
		MapData.save_data(data)
		# Monitor.getInstance().reload_map_data()
		return create_response_message("Sửa thành công", 200)



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