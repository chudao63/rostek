from .common import *
from sqlalchemy import and_
import logging
from app import db

class DbBaseModel:
	"""Add some database class method for SQLAlchemy

	"""
	@classmethod
	def new_from_dict(cls, _dict):
		"""
			create new object with dict data input
		"""
		output = cls()
		for key in _dict:
			if hasattr(output, key):
				setattr(output, key, _dict[key])
		return output
	
	@staticmethod
	def add_new( _new):
		"""
			Add new object to db 
		"""
		db.session.add(_new)
		db.session.commit()

	@classmethod
	def add_new_from_dict(cls, _dict):
		"""
			create new object with dict data input, and import to database
		"""
		output = cls()
		for key in _dict:
			if hasattr(output, key):
				setattr(output, key, _dict[key])
		logging.info(output)
		db.session.add(output)
		db.session.commit()
		return output

	@classmethod
	def update_from_dict(cls, _dict):
		"""
			create new object with dict data input
		"""
		finder = cls.query.get(_dict["id"])
		assert finder is not None, "Data not in DB"
		_dict.pop("id")
		for key in _dict:
			if hasattr(finder, key):
				setattr(finder, key, _dict[key])
		db.session.add(finder)
		db.session.commit()
		
	@classmethod
	def delete_by_list_id(cls, _listid):
		cls.query.filter(cls.id.in_(_listid)).delete(synchronize_session=False)
		db.session.commit()

	@classmethod
	def delete_by_id(cls, _id):
		"""
			DELETE class object
		"""
		cls.query.filter(cls.id.in_([_id])).delete(synchronize_session=False)
		db.session.commit()

	
	@classmethod
	def find_by_dict(cls, _dict):
		"""
			find in dabtabase an row from dict
		"""
		_filter = []
		for key in _dict:
			if _dict[key]:
				_filter.append(getattr(cls,key) == _dict[key])
		output = cls.query.filter(and_(*_filter)).all()
		return output
	
	@classmethod
	def get_all_attr(cls):
		"""
			return list of column name
		"""
		return [c.name for c in cls.__table__.columns]
		
	@property
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}