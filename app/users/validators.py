from app.users.models import User, UserRole
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from utils.common import *

class UserValidate:
	@staticmethod
	def get_user():
		username = get_jwt_identity()
		return User.query.get(username)

	@classmethod
	def admin_level(cls,func):
		"""
			CHECK PERMISSION FOR ADMIN LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user = UserValidate.get_user()
			if user:
				if user.role_id == "admin":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner

	@classmethod
	def manager_level(cls,func):
		"""
			CHECK PERMISSION FOR MANAGER LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user =  UserValidate.get_user()
			if user:
				if user.role_id == "manager":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner

	@classmethod
	def admin_manager_level(cls,func):
		"""
			CHECK PERMISSION FOR MANAGER OR MANAGER LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user = UserValidate.get_user()
			if user:
				if user.role_id == "manager" or user.role_id == "admin":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner

	@classmethod
	def qc_level(cls,func):
		"""
			CHECK PERMISSION FOR MANAGER LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user = UserValidate.get_user()
			if user:
				if user.role_id == "qc":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner
	
	@classmethod
	def tech_level(cls,func):
		"""
			CHECK PERMISSION FOR MANAGER LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user = UserValidate.get_user()
			if user:
				if user.role_id == "tech":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner
	
	@classmethod
	def tech_qc_level(cls,func):
		"""
			CHECK PERMISSION FOR MANAGER LEVEL
		"""
		@jwt_required()
		def inner(cls):
			user = UserValidate.get_user()
			if user:
				if user.role_id == "tech" or user.role_id == "qc":
					return func(cls)
				return create_response_message("Permission dinied",400)
			return create_response_message("Invalid user", 401)
		return inner