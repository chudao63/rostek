from logging import log
import logging
import re
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.functions import ReturnTypeFromArgs, count
from app.models.map import Map
from app.models.mission import Mission
from app.models.position import Position
from app.models.step import Step
from utils.apimodel import BaseApiPagination, ApiBase, ApiCommon
from flask_restful import Resource, reqparse, request
import os, sys
from flask import send_from_directory
from app.models.map import Map, MapData
from app import  db
from utils.common import object_as_dict, create_response_message

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
        Xóa img trên db
        URL: '/deleteimage'
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

<<<<<<< HEAD
		if args['id']:
			deleteImage = Map.query.filter(Map.id == args['id']).one()
			db.session.delete(deleteImage)
			db.session.commit()
			return create_response_message("Xóa thành công", 200)
		
=======
        if args['id']:
            deleteImage = Map.query.filter(Map.id == args['id']).one()
            db.session.delete(deleteImage)
            db.session.commit()
            return create_response_message("Xóa thành công", 200)
        
>>>>>>> 18e7651b8d3fe9f2172eb02efccb36b9a2981f34
class ActiveMapDataApi(ApiBase):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
=======
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
    def patch(self):
        """
        CHUYỂN ĐỔI DỮ LIỆU MAP ĐANG SỬ DỤNG
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
class CreateMapDataApi(ApiBase):
    @ApiBase.exception_error
    def post(self):
        """
        Thêm một Map Data mới
        URL: '/create-mapdata'
        Method: POST
        """
        data = request.get_json(force = True)
        map = MapData()
        for indexData in data:
            if indexData == 'description':
                map = MapData(description = data['description'])
        db.session.add(map)
        db.session.commit()
        return create_response_message("Tạo mới thành công", 200)

class PointApi(ApiBase):
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

        data =request.get_json(force = True)
        pointDbs = Position.query.all()

        for dataIndex in data['points']:
            if 'id' in dataIndex:
                point = Position.query.get(dataIndex['id'])
                point.x = dataIndex['x']
                point.y = dataIndex['y']
                point.name = dataIndex['name']
                point.type = dataIndex['type']
                point.map_data_id = dataIndex['map_data_id']
                db.session.add(point)
                db.session.commit()
            else:
                for pointDb in pointDbs:
                    if pointDb.name == dataIndex['name']:
                        return create_response_message(f"Tên {dataIndex['name']} đã tồn tại", 409)
                position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
                db.session.add(position)
                db.session.commit()
        return create_response_message("Sửa map_data thành công", 200)



        # data = request.get_json(force=True)
        # points = Position.query.all()
        
        # for dataIndex in data['points']:
        # 	logging.warning(dataIndex)
        # 	for point in points:
        # 		if point.name == dataIndex['name']:
        # 			return create_response_message(f"Tên {point.name} đã tồn tại", 409)
        # 	position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
        # 	db.session.add(position)
        # db.session.commit()

            
        # return create_response_message("Thêm điểm thành công", 200)
#>>>>>>> 499da75c48069d4aa7bd96586f1725825b3f56a4
    
    
    @ApiBase.exception_error
    def delete(self):
        """
        Xóa một điểm
        URL:'/point'
        """
        data = request.get_json(force = True)
        position = Position.query.get(data['id'])
        missions = Mission.query.all()
        steps = Step.query.filter(or_((Step.start_point == data['id']), (Step.end_point == data['id']))).all()
        for mission in missions:
            for index in mission.steps:
                if index.id == data['id']:
                    while len(mission.steps):
                        mission.steps.pop(0)
                        db.session.add(mission)
                        db.session.commit()

        for step in steps:
            logging.warning(step)
            if step.start_point or step.end_point == data['id']:
                stepId = Step.query.get(step.id)
                db.session.delete(stepId)
                db.session.commit()

        db.session.delete(position)
        db.session.commit()
        return create_response_message("Xóa thành công", 200)

<<<<<<< HEAD
<<<<<<< HEAD
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
                positionDict = position.as_dict
                mapDataDict['positions'].append(positionDict)
            output.append(mapDataDict)
        return output

    @ApiBase.exception_error
    def post(self):
        """
        Thêm một Map Data mới
        URL: '/create-mapdata'
        Method: POST
        """
        data = request.get_json(force = True)
        map = MapData()
        for indexData in data:
            if indexData == 'description':
                map = MapData(description = data['description'])
        db.session.add(map)
        db.session.commit()
        return create_response_message("Tạo mới thành công", 200)
        

    # @ApiBase.exception_error
    # def post(self):
    # 	"""
    # 	Thêm các điểm mới vào MapData
    # 	URL: '/mapdata'
    # 	Method: POST
    # 	"""
    # 	data = request.get_json(force=True)
    # 	mapData = MapData.query.get(data['id'])
    # 	for positionIndex in data['positions']:
    # 		position = Position.query.get(positionIndex)
    # 		mapData.positions.append(position)
    # 		db.session.add(mapData)
    # 		db.session.commit()
    # 	return create_response_message("Thêm mới thành công", 200)


    # @ApiBase.exception_error
    # def delete(self):
    # 	"""
    # 	Xóa một điểm được chọn trong Map data - Position
    # 	URL:'/mapdata'
    # 	Method: delete
    # 	"""

        
    # 	count = 0
    # 	data = request.get_json(force = True)
    # 	mapData = MapData.query.get(data['id'])
    # 	assert mapData is not None, f"MapData {data['id']} không tồn tại"

    # 	for mapDataIndex in mapData.positions: # tìm ra tất cả các position đang có trong map_data[id]
    # 		if mapDataIndex.id == data['position']:
    # 			mapData.positions.pop(count)
    # 			db.session.add(mapData)
    # 			db.session.commit()
    # 			return create_response_message("Xóa thành công", 200)
    # 		count = count + 1 
=======
	def patch(self):
		"""
		CHUYỂN ĐỔI DỮ LIỆU MAP ĐANG SỬ DỤNG
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
class CreateMapDataApi(ApiBase):
	@ApiBase.exception_error
	def post(self):
		"""
		Thêm một Map Data mới
		URL: '/create-mapdata'
		Method: POST
		"""
		data = request.get_json(force = True)
		map = MapData()
		for indexData in data:
			if indexData == 'description':
				map = MapData(description = data['description'])
		db.session.add(map)
		db.session.commit()
		return create_response_message("Tạo mới thành công", 200)

class PointApi(ApiBase):
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

		data =request.get_json(force = True)
		pointDbs = Position.query.all()

		for dataIndex in data['points']:
			if 'id' in dataIndex:
				point = Position.query.get(dataIndex['id'])
				point.x = dataIndex['x']
				point.y = dataIndex['y']
				point.name = dataIndex['name']
				point.type = dataIndex['type']
				point.map_data_id = dataIndex['map_data_id']
				db.session.add(point)
				db.session.commit()
			else:
				for pointDb in pointDbs:
					if pointDb.name == dataIndex['name']:
						return create_response_message(f"Tên {dataIndex['name']} đã tồn tại", 409)
				position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
				db.session.add(position)
				db.session.commit()
		return create_response_message("Sửa map_data thành công", 200)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD


		# data = request.get_json(force=True)
		# points = Position.query.all()
		
		# for dataIndex in data['points']:
		# 	logging.warning(dataIndex)
		# 	for point in points:
		# 		if point.name == dataIndex['name']:
		# 			return create_response_message(f"Tên {point.name} đã tồn tại", 409)
		# 	position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
		# 	db.session.add(position)
		# db.session.commit()

			
		# return create_response_message("Thêm điểm thành công", 200)
<<<<<<< HEAD
<<<<<<< HEAD
#>>>>>>> 499da75c48069d4aa7bd96586f1725825b3f56a4
	
=======
>>>>>>> 18e7651b8d3fe9f2172eb02efccb36b9a2981f34
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
	
	@ApiBase.exception_error
	def delete(self):
		"""
		Xóa một điểm
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
		URL:'/point'
		"""
		data = request.get_json(force = True)
		position = Position.query.get(data['id'])
=======
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
		Khi xóa một điểm ->  Xóa step chứa điểm đó -> Xóa các bước của mission chứa step đó
		URL:'/point'
		METHOD: DELETE
		"""
		data = request.get_json(force = True)
		position = Position.query.get(data['id'])
		assert position is not None, f"Point {data['id']} không tồn tại"
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 18e7651b8d3fe9f2172eb02efccb36b9a2981f34
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
		missions = Mission.query.all()
		steps = Step.query.filter(or_((Step.start_point == data['id']), (Step.end_point == data['id']))).all()
		for mission in missions:
			for index in mission.steps:
				if index.id == data['id']:
					while len(mission.steps):
						mission.steps.pop(0)
						db.session.add(mission)
						db.session.commit()

		for step in steps:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
			logging.warning(step)
=======
>>>>>>> 18e7651b8d3fe9f2172eb02efccb36b9a2981f34
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
			if step.start_point or step.end_point == data['id']:
				stepId = Step.query.get(step.id)
				db.session.delete(stepId)
				db.session.commit()

		db.session.delete(position)
		db.session.commit()
		return create_response_message("Xóa thành công", 200)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 18e7651b8d3fe9f2172eb02efccb36b9a2981f34
=======

>>>>>>> parent of 257be39... update robot
=======

>>>>>>> parent of 257be39... update robot
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
				positionDict = position.as_dict
				mapDataDict['positions'].append(positionDict)
			output.append(mapDataDict)
		return output
<<<<<<< HEAD
<<<<<<< HEAD
		

	@ApiBase.exception_error
	def patch(self):
		"""
		CHUYỂN ĐỔI DỮ LIỆU MAP ĐANG SỬ DỤNG
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


class CreateMapDataApi(ApiBase):
	@ApiBase.exception_error
	def post(self):
		"""
		Thêm một Map Data mới
		URL: '/create-mapdata'
		Method: POST
		"""
		data = request.get_json(force = True)
		map = MapData()
		for indexData in data:
			if indexData == 'description':
				map = MapData(description = data['description'])
		db.session.add(map)
		db.session.commit()
		return create_response_message("Tạo mới thành công", 200)

class PointApi(ApiBase):
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

		data =request.get_json(force = True)
		pointDbs = Position.query.all()

		for dataIndex in data['points']:
			if 'id' in dataIndex:
				point = Position.query.get(dataIndex['id'])
				point.x = dataIndex['x']
				point.y = dataIndex['y']
				point.name = dataIndex['name']
				point.type = dataIndex['type']
				point.map_data_id = dataIndex['map_data_id']
				db.session.add(point)
				db.session.commit()
			else:
				for pointDb in pointDbs:
					if pointDb.name == dataIndex['name']:
						return create_response_message(f"Tên {dataIndex['name']} đã tồn tại", 409)
				position = Position(x = dataIndex['x'], y = dataIndex['y'], name = dataIndex['name'], type = dataIndex['type'], map_data_id = dataIndex['map_data_id'])
				db.session.add(position)
				db.session.commit()
		return create_response_message("Sửa map_data thành công", 200)

=======
	
>>>>>>> parent of b89d34c... Update Modles Robot
=======
	
>>>>>>> parent of b89d34c... Update Modles Robot
	
	@ApiBase.exception_error
	def delete(self):
		"""
		Xóa một điểm
		URL:'/point'
		"""
		data = request.get_json(force = True)
		position = Position.query.get(data['id'])
		missions = Mission.query.all()
		steps = Step.query.filter(or_((Step.start_point == data['id']), (Step.end_point == data['id']))).all()
		for mission in missions:
			for index in mission.steps:
				if index.id == data['id']:
					while len(mission.steps):
						mission.steps.pop(0)
						db.session.add(mission)
						db.session.commit()

		for step in steps:
			logging.warning(step)
			if step.start_point or step.end_point == data['id']:
				stepId = Step.query.get(step.id)
				db.session.delete(stepId)
				db.session.commit()

		db.session.delete(position)
		db.session.commit()
		return create_response_message("Xóa thành công", 200)


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
				positionDict = position.as_dict
				mapDataDict['positions'].append(positionDict)
			output.append(mapDataDict)
		return output
=======
>>>>>>> parent of 257be39... update robot
=======
>>>>>>> parent of 257be39... update robot
		

	# @ApiBase.exception_error
	# def post(self):
	# 	"""
	# 	Thêm các điểm mới vào MapData
	# 	URL: '/mapdata'
	# 	Method: POST
	# 	"""
		# data = request.get_json(force=True)
		# mapData = MapData.query.get(data['id'])
		# for positionIndex in data['positions']:
		# 	position = Position.query.get(positionIndex)
		# 	mapData.positions.append(position)
		# 	db.session.add(mapData)
		# 	db.session.commit()
		# return create_response_message("Thêm mới thành công", 200)


	# @ApiBase.exception_error
	# def delete(self):
	# 	"""
	# 	Xóa một điểm được chọn trong Map data - Position
	# 	URL:'/mapdata'
	# 	Method: delete
	# 	"""

		
	# 	count = 0
	# 	data = request.get_json(force = True)
	# 	mapData = MapData.query.get(data['id'])
	# 	assert mapData is not None, f"MapData {data['id']} không tồn tại"

	# 	for mapDataIndex in mapData.positions: # tìm ra tất cả các position đang có trong map_data[id]
	# 		if mapDataIndex.id == data['position']:
	# 			mapData.positions.pop(count)
	# 			db.session.add(mapData)
	# 			db.session.commit()
	# 			return create_response_message("Xóa thành công", 200)
	# 		count = count + 1 
>>>>>>> parent of 257be39 (update robot)
=======
class MapDataApi(ApiBase):
=======
class MapDataApi(ApiBase):
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
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
                positionDict = position.as_dict
                mapDataDict['positions'].append(positionDict)
            output.append(mapDataDict)
        return output

    @ApiBase.exception_error
    def post(self):
        """
        Thêm một Map Data mới
        URL: '/create-mapdata'
        Method: POST
        """
        data = request.get_json(force = True)
        map = MapData()
        for indexData in data:
            if indexData == 'description':
                map = MapData(description = data['description'])
        db.session.add(map)
        db.session.commit()
        return create_response_message("Tạo mới thành công", 200)
        

    # @ApiBase.exception_error
    # def post(self):
    # 	"""
    # 	Thêm các điểm mới vào MapData
    # 	URL: '/mapdata'
    # 	Method: POST
    # 	"""
    # 	data = request.get_json(force=True)
    # 	mapData = MapData.query.get(data['id'])
    # 	for positionIndex in data['positions']:
    # 		position = Position.query.get(positionIndex)
    # 		mapData.positions.append(position)
    # 		db.session.add(mapData)
    # 		db.session.commit()
    # 	return create_response_message("Thêm mới thành công", 200)


    # @ApiBase.exception_error
    # def delete(self):
    # 	"""
    # 	Xóa một điểm được chọn trong Map data - Position
    # 	URL:'/mapdata'
    # 	Method: delete
    # 	"""

        
    # 	count = 0
    # 	data = request.get_json(force = True)
    # 	mapData = MapData.query.get(data['id'])
    # 	assert mapData is not None, f"MapData {data['id']} không tồn tại"

    # 	for mapDataIndex in mapData.positions: # tìm ra tất cả các position đang có trong map_data[id]
    # 		if mapDataIndex.id == data['position']:
    # 			mapData.positions.pop(count)
    # 			db.session.add(mapData)
    # 			db.session.commit()
    # 			return create_response_message("Xóa thành công", 200)
    # 		count = count + 1 
<<<<<<< HEAD
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05
=======
>>>>>>> 2c9b1bd4ba15b6639053861f8d6f94417747ea05

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
				positionDict = position.as_dict
				mapDataDict['positions'].append(positionDict)
			output.append(mapDataDict)
		return output

	@ApiBase.exception_error
	def post(self):
		"""
		Thêm một Map Data mới
		URL: '/create-mapdata'
		Method: POST
		"""
		data = request.get_json(force = True)
		map = MapData()
		for indexData in data:
			if indexData == 'description':
				map = MapData(description = data['description'])
		db.session.add(map)
		db.session.commit()
		return create_response_message("Tạo mới thành công", 200)
		

	# @ApiBase.exception_error
	# def post(self):
	# 	"""
	# 	Thêm các điểm mới vào MapData
	# 	URL: '/mapdata'
	# 	Method: POST
	# 	"""
	# 	data = request.get_json(force=True)
	# 	mapData = MapData.query.get(data['id'])
	# 	for positionIndex in data['positions']:
	# 		position = Position.query.get(positionIndex)
	# 		mapData.positions.append(position)
	# 		db.session.add(mapData)
	# 		db.session.commit()
	# 	return create_response_message("Thêm mới thành công", 200)


	# @ApiBase.exception_error
	# def delete(self):
	# 	"""
	# 	Xóa một điểm được chọn trong Map data - Position
	# 	URL:'/mapdata'
	# 	Method: delete
	# 	"""

		
	# 	count = 0
	# 	data = request.get_json(force = True)
	# 	mapData = MapData.query.get(data['id'])
	# 	assert mapData is not None, f"MapData {data['id']} không tồn tại"

	# 	for mapDataIndex in mapData.positions: # tìm ra tất cả các position đang có trong map_data[id]
	# 		if mapDataIndex.id == data['position']:
	# 			mapData.positions.pop(count)
	# 			db.session.add(mapData)
	# 			db.session.commit()
	# 			return create_response_message("Xóa thành công", 200)
	# 		count = count + 1 









