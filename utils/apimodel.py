from flask_restful import Resource, request, reqparse
import logging
from sqlalchemy import and_
from app import db
from utils.common import *
from utils.vntime import VnTimestamp

class ApiBase(Resource):
	def request_parser(self,args, required_args):
		"""	Parser data from request
		
		"""
		parser = reqparse.RequestParser()
		for arg in args:
			if arg in required_args:
				parser.add_argument(arg, help = 'This field cannot be blank', required = True)
			else:
				parser.add_argument(arg, required = False)
		data = parser.parse_args()
		return data

	def json_parser(self, args, required_args):
		"""Parser Json data from Json body

		Returns:
			{
				validate : True if data is good
				message : return message if validate false
				data : data parser from json requests
			}
		"""

		data = request.get_json(force=True)
		
		_responseMessage  = {}
		_responseCode = 200
		
		for key in data:
			if key not in data:
				data.pop(key)
  
		if required_args:
			for arg in required_args:
				if arg not in data:
					_responseMessage[arg] = "This field can't be blank"
					_responseCode = 404

		_validate = False if _responseMessage else True

		return {
			"validate" : _validate,
			"message": create_response_message(_responseMessage, _responseCode),
			"data" : data
		}


	def json_parsers(self, args, required_args):
		"""Parser Json multiple data from Json body

		Returns:
			{
				validate : True if data is good
				message : return message if validate false
				data : data parser from json requests
			}
		"""

		datas = request.get_json(force=True)
		_responseMessage  = {}
		_responseCode = 200
		for data in datas:
			for key in data:
				if key not in data:
					data.pop(key)
	
			if required_args:
				for arg in required_args:
					if arg not in data:
						_responseMessage[arg] = "This field can't be blank"
						_responseCode = 404

			_validate = False if _responseMessage else True
		return {
			"validate" : _validate,
			"message": create_response_message(_responseMessage, _responseCode),
			"data" : datas
		}
	
	@classmethod
	def exception_error(cls,func):
		"""
			DECORATOR FOR TRY AND EXCEPTION ERROR
		"""
		def inner(cls):
			try:
				return func(cls)
			except AssertionError as error:
				logging.error(error)
				return create_response_message(str(error),409)
			# except exc.IntegrityError as e:
			# 	logging.error(str(e))
			# 	return create_response_message(str(e.orig.args[1]),409)
			except Exception as e:
				# logging.error(e.File)
				logging.error(str(e))
				if "Missing claim" in str(e):
					return create_response_message("Authentication error",401)
				logging.critical(e, exc_info=True)
				return create_response_message(str(e),409)
		return inner

class ApiCommon(ApiBase):
	"""API BASE included : POST/GET/PATCH/DELETE for common apis

	"""
	def __init__(self, ModelType, rootUrl):
		self.ModelType = ModelType
		self.rootUrl = rootUrl

	@ApiBase.exception_error
	def get_list_id(self):
		ids = list(map(lambda x: x[0], db.session.query(self.ModelType.id).all()))
		# list_id = db.session.query(self.ModelType.id).all()
		return ids

	@ApiBase.exception_error
	def get(self):
		"""
			GET: With any params
		"""
		args = self.ModelType.get_all_attr()
		required_args = []
		data = self.request_parser(args, required_args)
		return object_as_dict(self.ModelType.find_by_dict(data))
	
	@ApiBase.exception_error
	def post(self):
		"""
			POST: Required ID in data
		"""
		args = self.ModelType.get_all_attr()
		# required_args = ["id"]
		required_args = []
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			self.ModelType.add_new_from_dict(data)
			return create_response_message("Thêm mới thành công", 200)
		return parser["message"]

	@ApiBase.exception_error
	def post_with_required_args(self, required_args):
		"""
			POST: dynamic required
		"""
		args = self.ModelType.get_all_attr()
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			self.ModelType.add_new_from_dict(data)
			return create_response_message("Thêm mới thành công", 200)
		return parser["message"]

	@ApiBase.exception_error
	def patch(self):
		"""
			POST: Required ID in data
		"""
		args =  self.ModelType.get_all_attr()
		required_args = ["id"]
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			self.ModelType.update_from_dict(data)
			return create_response_message("Sửa thành công", 200)
		return parser["message"]

	@ApiBase.exception_error
	def delete(self):
		"""
			DELETE: Required ID or list ID in data
		"""
		args = ["id"]
		required_args = []
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			if type(data["id"]) is list:
				self.ModelType.delete_by_list_id(data["id"])
				return create_response_message("Xóa thành công", 200)
			else:
				self.ModelType.delete_by_id(data["id"])
				return create_response_message("Xóa thành công", 200)

class BaseApiGetListId(ApiCommon):
	def get(self):
		"""
		Trả ra dữ liệu get bao gồm cả listId và details
		"""
		args = self.ModelType.get_all_attr()
		required_args = []
		data = self.request_parser(args, required_args)
		datas = self.ModelType.find_by_dict(data)
		if '/list_id' in request.path:
			return self.get_list_id()
		elif '/detail' in request.path:
			_list = []
			for data in datas:
				_list.append(data.get_detail())
			return _list
		else:
			return object_as_dict(datas)

class BaseApiPagination(ApiCommon):
	def pagination(self, required_args = [], modelTime = None, querySort = None):
		"""Trả ra dữ liệu phân trang

		Args:
			required_args (list, optional): mảng các key bắt buộc. Defaults to [].
			modelTime (ModelField, optional): Field cần lọc theo thời gian. Defaults to None.
			querySort (Query sort, optional): Phần tử cần sắp xếp(tăng hoặc giảm). Defaults to None.

		Returns:
			dict: Dữ liệu phân trang
		"""
		modelKeys = self.ModelType.get_all_attr()
		args = modelKeys.copy()
		args += ["from", "to", "date", "page", "number_of_page"]
		data = self.request_parser(args, required_args)
		#filter date time
		_filter = []
		if modelTime:
			if data["date"]:
				timeFrom = VnTimestamp.day_start(data["date"])
				timeTo = VnTimestamp.day_end(data["date"])
			else:
				timeFrom = VnTimestamp.today_start()
				timeTo = VnTimestamp.today_end()
			_filter.append(modelTime.between(timeFrom, timeTo))
		#filter by model type
		for key in modelKeys:
			if key in data:
				if data[key]:
					_filter.append(getattr(self.ModelType,key) == data[key])
		#pagination
		if data['page']:
			page = int(data['page']) - 1
			number_of_page = int(data['number_of_page']) if data['number_of_page'] else 10
		else:
			page = 0
			number_of_page = 10000
		if querySort:
			query = self.ModelType.query.filter(and_(*_filter)).order_by(querySort)
		else:
			query = self.ModelType.query.filter(and_(*_filter))

		total = len(query.all())
		orders = query.limit(
			number_of_page
		).offset(page*number_of_page).all()
		return {
			"data" : object_as_dict(orders),
			"page_info" : {
				"current" : page + 1,
				"total" : total
			}
		}
	def get(self):
		return self.pagination()

class BaseConfigureApi(ApiBase):
	"""
	Base API for read/write configure file
	"""
	def get(self):
		if '/filter' in request.path:
			return self.get_filter()
		elif '/post' in request.path:
			return self.get_post()
		elif '/patch' in request.path:
			return self.get_patch()
		elif '/delete' in request.path: 
			return self.get_delete()

	def post(self):
		args = ["data"]
		parser = self.json_parser(args, [])
		data = parser["data"]
		if '/post' in request.path:
			self.set_post(data)
		elif '/patch' in request.path:
			self.set_post(data)
		elif '/delete' in request.path:
			self.set_delete(data)
		return "Update file delete thành công"