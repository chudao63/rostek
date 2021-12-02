import logging
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import false, true
from utils.dbmodel import DbBaseModel
from app import db
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import validates

class UserRole(db.Model, DbBaseModel):
	__tablename__ = "userrole"
	id 		= Column(Integer,  primary_key=True, autoincrement=True, nullable=False)
	name	= Column(String(200), nullable=False)
	label 	= db.Column(db.Unicode(255), server_default=u'')  # for display purposes
	users 	= relationship('User', backref="role", lazy=True)

	def __str__(self):
		return self.id

class User(db.Model, DbBaseModel):
	__tablename__ = "user"
	id    			= Column(String(250),  primary_key=True,nullable=False)
	username		= Column(String(250), unique=False, nullable=False)
	__password    	= Column("password",String(200), unique=False, nullable=False)
	name        	= Column(String(100), unique=False, nullable=False)
	email       	= Column(String(100), unique=False, nullable=False)
	phone       	= Column(String(15),  unique=False, nullable=True)
	role_id	        = Column(Integer,  ForeignKey('userrole.id'))
	active 			= Column(Boolean, default = True, nullable=False)
	description 	= Column(String(100), unique=False, nullable=True)

	@validates('email')
	def validate_email(self, key, address):
		assert '@' in address  ,"Must be have @ in email address"
		return address
	
	@validates('phone')
	def validate_phone(self, key, phone):
		# assert len(phone) >= 9 and phone.isdigit()  ,"Số điện thoại không đúng"
		return phone

	def __str__(self):
		return self.id
	
	@property
	def password(self):
		return self.__password  

	@password.setter
	def password(self, password):
		# SpecialSym =['$', '@', '#', '%']
		# if len(password) < 8:
		# 	assert False, 'Chiều dài kí tự phải lớn hơn 8'
		# if not any(char.isupper() for char in password):
		# 	assert False, 'Mật khẩu phải có ít nhất 1 kí tự viết hoa'
		# if not any(char in SpecialSym for char in password):
		# 	assert False, 'Mất khẩu phải có ít nhất 1 kí tự đặc biệt $@#'
		self.__password = sha256.hash(password)
	
	# @property
	# def role_id(self):
	# 	return self._role_id  

	# @password.setter
	# def password(self, role_id):
		
	# 	self._role_id = role_id
	
	
	def verify_password(self,password):
		"""verify password for user

		Args:
			password (String): string input

		Returns:
			True/False: validate password
		"""
		return sha256.verify(password, self.password)
	
	@staticmethod
	def get_all_username_by_role(role):
		role_id = UserRole.query.filter(UserRole.name == role).first()
		if role_id:
			logging.warning(role_id)
			users = db.session.query(User.id).filter(User.role_id == role_id.id)
			list_user = []
			for user in users:
				list_user.append(user.id)
			return list_user
		assert list_user, "user not exist"

class RevokedTokenUser(db.Model, DbBaseModel):
	__tablename__ = "revokedtoken"
	jti = Column(String(500), primary_key=True, unique=True,  nullable=False)


class UserTableColumn(db.Model, DbBaseModel):
	__tablename__ = "user_table_column"
	id    			= Column(Integer,  primary_key=True, autoincrement=True, nullable=False)
	username 		= Column(String(200), nullable=False)
	table			= Column(String(50), unique=False, nullable=False)
	data			= Column(String(1000), unique=False, nullable=False)

db.create_all()