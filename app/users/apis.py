from humanfriendly.terminal import message, warning
from .consts import *
from .models import *
from .validators import UserValidate
from utils.common import *
from utils.apimodel import ApiCommon, ApiBase, BaseApiGetListId
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, request
from passlib.hash import pbkdf2_sha256 as sha256
import logging
from sqlalchemy import exc, and_, func

class UserApi(ApiCommon):
	"""URL: /user

	"""
	def __init__(self):
		ApiCommon.__init__(self, User, "/user")

	@UserValidate.admin_level
	def get(self):
		if "/all" in request.path:
			parser = self.request_parser(['current', 'number_of_page', 'username', 'name'], [])
			# users = User.query.all()
			_filter = []
			if parser['username']:
				_filter.append(User.id.contains(parser['username']))
			if parser['name']:
				_filter.append(User.name.contains(parser['name']))
			if parser['current']:
				pageNumber = int(parser['current']) - 1
				quantityInPage = int(parser['number_of_page']) if parser['number_of_page'] else 10
				total = db.session.query(func.count(User.id)).filter(and_(*_filter)).scalar()
				users= User.query.filter(and_(*_filter)).limit(quantityInPage).offset(pageNumber*quantityInPage).all()
			else:
				if parser['number_of_page']:
					quantityInPage = parser['number_of_page']
				else:
					quantityInPage = 10
				pageNumber = 0
				users= User.query.filter(and_(*_filter)).all()
				total = len(users)
			data = []
			for user in  users:
				user_dict = as_dict(user)
				user_dict["password"] = ""
				userRole = UserRole.query.get(user_dict["role_id"])
				user_dict["role_name"] = userRole.name
				data.append(user_dict)
			return {
				"data" : data,
				"page_info" : {
					"current" : pageNumber + 1,
					"number_of_page" : int(quantityInPage),
					"total" : total
				}
			}
		else:
			parser = self.request_parser(['current', 'number_of_page', 'username', 'name'], [])
			_filter = []
			_filter.append(User.role_id == 1 or User.role_id == 2)
			if parser['username']:
				_filter.append(User.id.contains(parser['username']))
			if parser['name']:
				_filter.append(User.name.contains(parser['name']))
			if parser['current']:
				pageNumber = int(parser['current']) - 1
				quantityInPage = int(parser['number_of_page']) if parser['number_of_page'] else 10
				total = db.session.query(func.count(User.id)).filter(and_(*_filter)).scalar()
				users= User.query.filter(and_(*_filter)).limit(quantityInPage).offset(pageNumber*quantityInPage).all()
			else:
				if parser['number_of_page']:
					quantityInPage = parser['number_of_page']
				else:
					quantityInPage = 10
				pageNumber = 0
				users= User.query.filter(and_(*_filter)).all()
				total = len(users)
			data = []
			for user in  users:
				user_dict = as_dict(user)
				user_dict["password"] = ""
				userRole = UserRole.query.get(user_dict["role_id"])
				user_dict["role_name"] = userRole.name
				data.append(user_dict)
			return {
				"data" : data,
				"page_info" : {
					"current" : pageNumber + 1,
					"number_of_page" : int(quantityInPage),
					"total" : total
				}
			}

	@UserValidate.admin_level
	@ApiCommon.exception_error
	def post(self):
		args = ["username", "password", "name", "email", "phone", "role_name", "level", "active", "enterprise", "description"]
		required_args = ["password", "username"]
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			data["id"] = data["username"].lower().strip()
			userRole = UserRole.query.filter(UserRole.name == data["role_id"]).first()
			assert userRole, f"Không có role tên {data['role_id']}"
			data["role_id"] = userRole.id
			User.add_new_from_dict(data)
			return create_response_message(f"Tạo user {data['id']} thành công!", 200)
		return parser["message"]

	@UserValidate.admin_level
	@ApiCommon.exception_error
	def patch(self): 
		args = ["id", "username", "password", "name", "email", "phone", "role_name", "level", "active", "enterprise", "description"]
		args.append("admin_password")
		required_args = ["id", "admin_password"]
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			data = parser["data"]
			admin_password = data.pop("admin_password")
			admin = User.query.get("admin")
			assert admin.verify_password(admin_password), "Mật khẩu cho account admin không chính xác"
			userRole = UserRole.query.filter(UserRole.name == data["role_name"]).first()
			assert userRole, f"Không có role tên {data['role_name']}"
			data["role_id"] = userRole.id
			self.ModelType.update_from_dict(data)
			return create_response_message("Thay đổi thành công!",200)
		return parser["message"]

	@UserValidate.admin_level
	@ApiCommon.exception_error
	def delete(self):
		args = ["id", "admin_password"]
		parser = self.json_parser(args, args)
		if parser["validate"]:
			data = parser["data"]
			admin_password = data.pop("admin_password")
			admin = User.query.get("admin")
			assert admin.verify_password(admin_password), "Mật khẩu cho account admin không chính xác"
			if type(data["id"]) is list:
				ind = 0
				for user_id in data["id"]:
					user = User.query.get(user_id)
					assert user, f"Không có user {data['id'][ind]}"
					ind += 1
				self.ModelType.delete_by_list_id(data["id"])
			else:
				user = User.query.get(data["id"])
				assert user, f"Không có user {data['id']}"
				self.ModelType.delete_by_id(data["id"])
			return create_response_message("Xóa thành công!",200)
		else:
			return parser["message"]

# class UserManagerApi(ApiCommon):
# 	"""URL: /user

# 	"""
# 	def __init__(self):
# 		ApiCommon.__init__(self, User, "/usermanager")

# 	@jwt_required()
# 	@ApiCommon.exception_error
# 	def get(self):
# 		username = get_jwt_identity()
# 		parser = self.request_parser(['page', 'number_of_page', 'id', 'name'], [])
# 		_filter = []
# 		user = User.query.get(username)
# 		if user.role_id == "manager":
# 			_filter.append(User.enterprise == user.enterprise)
# 			if parser['id']:
# 				_filter.append(User.id.contains(parser['id']))
# 			if parser['name']:
# 				_filter.append(User.name.contains(parser['name']))
# 			if parser['page']:
# 				pageNumber = int(parser['page']) - 1
# 				quantityInPage = int(parser['number_of_page']) if parser['number_of_page'] else 10
# 				total = db.session.query(func.count(User.id)).filter(and_(*_filter)).scalar()
# 				users= User.query.filter(and_(*_filter)).limit(quantityInPage).offset(pageNumber*quantityInPage).all()
# 			else:
# 				pageNumber = 0
# 				users= User.query.filter(and_(*_filter)).all()
# 				total = len(users)
# 			data = []
# 			for user in  users:
# 				user_dict = as_dict(user)
# 				data.append(user_dict)
# 				user_dict["password"] = ""
# 				# logging.warning(out_dict["id"])
# 			return {
# 				"data" : data,
# 				"page_info" : {
# 					"current" : pageNumber + 1,
					# "number_of_page" : parser['number_of_page'],
# 					"total" : total
# 				}
# 			} 
# 		return f"Không có user"

# 	@jwt_required()
# 	@ApiCommon.exception_error
# 	def post(self):
# 		args = ["id", "password", "name", "email", "phone", "role_id", "level", "active", "description"]
# 		required_args = ["password", "id"]
# 		parser = self.json_parser(args, required_args)
# 		username = get_jwt_identity()
# 		user = User.query.get(username)
# 		enterprise = user.enterprise
# 		if parser["validate"]:
# 			data = parser["data"]
# 			data["id"] = f'{data["id"].lower().strip()}_{enterprise.lower().strip()}'
# 			data["enterprise"] = enterprise
# 			User.add_new_from_dict(data)
# 			return create_response_message(f"Tạo user {data['id']} thành công!", 200)
# 		return parser["message"]

# 	@UserValidate.manager_level
# 	@ApiCommon.exception_error
# 	def patch(self): 
# 		args = ["id", "password", "name", "email", "phone", "role_id", "level", "acvite" ,"description", "manager_password"]
# 		required_args = ["id", "manager_password"]
# 		parser = self.json_parser(args, required_args)
# 		username = get_jwt_identity()
# 		manager = User.query.get(username)
# 		if parser["validate"]:
# 			data = parser["data"]
# 			manager_password = data.pop("manager_password")
# 			assert manager.verify_password(manager_password), "Mật khẩu cho account manager không chính xác"
# 			self.ModelType.update_from_dict(data)
# 			return create_response_message("Thay đổi thành công!",200)
# 		return parser["message"]

# 	@jwt_required()
# 	@ApiCommon.exception_error
# 	def delete(self):
# 		args = ["id", "manager_password"]
# 		parser = self.json_parser(args, args)
# 		username = get_jwt_identity()
# 		if parser["validate"]:
# 			data = parser["data"]
# 			manager_password = data.pop("manager_password")
# 			manager = User.query.get(username)
# 			assert manager.verify_password(manager_password), "Mật khẩu cho account manager không chính xác"
# 			if type(data["id"]) is list:
# 				self.ModelType.delete_by_list_id(data["id"])
# 			else:
# 				self.ModelType.delete_by_id(data["id"])
# 			return create_response_message("Xóa thành công!",200)
# 		else:
# 			return parser["message"]

		
class UserListApi(Resource):
	def get(self): 
		if '/user/list_id_tech' == request.path:
			return User.get_all_username_by_role("tech")
		elif '/user/list_id_manager' == request.path:
			return User.get_all_username_by_role("manager")

class UserRoleApi(BaseApiGetListId):
	"""URL: /userrole

	"""
	def __init__(self):
		ApiCommon.__init__(self, UserRole, "/userrole")

	@ApiCommon.exception_error
	def get(self):
		if "/list_name" in request.path:
			userRoles = UserRole.query.all()
			roleDict = []
			for userRole in userRoles:
				roleDict.append(userRole.name)
			return roleDict
		return BaseApiGetListId.get(self)

	@UserValidate.admin_level
	@ApiCommon.exception_error
	def post(self):
		args = ["name" , "label"]
		parser = self.json_parser(args, args)
		logging.warning(parser)
		if parser["validate"]:
			data = parser["data"]
			userRole = UserRole.query.filter(UserRole.name == data["name"]).first()
			assert not userRole, f"Đã có role {data['name']} này"
			db.session.add(UserRole(name= data["name"],    label = data["label"]))
			db.session.commit()
			return create_response_message(f"Thêm mới role {data['name']} thành công", 200)
		return parser["message"]

class UserLogin(ApiBase):
	"""URL: /login

	"""
	@ApiCommon.exception_error
	def post(self):
		args = ["username", "password"]
		required_args = ["username", "password"]
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			login_username = parser["data"]["username"]
			login_password = parser["data"]["password"]
			login_user = User.query.filter(User.id == login_username).first()
			if login_user:
				if login_user.verify_password(login_password):
					access_token = create_access_token(identity = login_username, expires_delta=ACCESS_EXP)
					refresh_token = create_refresh_token(identity = login_username, expires_delta=REFRESH_EXP)
					return {
						'msg': f'Logged in as {login_username}',
						'access_token': access_token,
						'refresh_token': refresh_token,
						'userrole': login_user.role_id
					}, 200
				else:
					return create_response_message("Sai mật khẩu", 401)
			return create_response_message("Không tìm thấy user", 404)
		return parser["message"]

class UserProfile(ApiBase):
	"""URL: /profile

	"""
	@jwt_required()
	@ApiCommon.exception_error
	def get(self):
		username = get_jwt_identity()
		print(username)
		currentUser = User.query.get(username)
		if currentUser:
			user_dict = object_as_dict(currentUser)
			user_dict.pop("password")
			return user_dict
		return create_response_message("Có lỗi xảy ra", 401)
	
	@jwt_required()
	@ApiCommon.exception_error
	def patch(self):
		"""
			PATH DATA FROM CURRENT USER
		"""
		args =  User.get_all_attr()
		required_args = ["id"]
		parser = self.json_parser(args, required_args)
		if parser["validate"]:
			username = get_jwt_identity()
			currentUser = User.query.get(username)
			data = parser["data"]
			if "old_password" in data and "new_password" in data:
				if currentUser.verify_password(data["old_password"]):
					data["password"] = sha256.hash(data["new_password"])
				else:
					return create_response_message("Mật khẩu cũ không chính xác", 409)
			currentUser.update_from_dict(data)
			return create_response_message("Cập nhật thành công", 200)
		return parser["message"]

class UserLogout(Resource):
	"""URL: /logout

	"""
	@jwt_required()
	@ApiCommon.exception_error
	def post(self):
		jti = get_jwt()['jti']
		token = RevokedTokenUser(jti=jti)
		RevokedTokenUser.add_new(token)
		return {'msg': 'Access token has been revoked'}

class UserRefreshToken(Resource):
	"""URL: /refresh_token

	"""
	@jwt_required(refresh=True)
	@ApiCommon.exception_error
	def post(self):      
		currentUser = get_jwt_identity()
		accessToken = create_access_token(identity = currentUser, expires_delta=ACCESS_EXP)
		return {'access_token': accessToken}

class UserRevokeRefreshToken(Resource):
	"""URL: /revoke_refresh_token

	"""
	@jwt_required(refresh=True)
	@ApiCommon.exception_error
	def post(self):
		jti = get_jwt()['jti']
		token = RevokedTokenUser(jti=jti)
		RevokedTokenUser.add_new(token)
		return {'msg': 'Refresh token has been revoked'}