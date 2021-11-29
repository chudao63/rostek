from sqlalchemy import Column, String
from utils.dbmodel import DbBaseModel
from app import db

class Example(db.Model, DbBaseModel):
	__tablename__ = "example"
	id 				= Column(String(50), primary_key=True, nullable=False, unique = True)
	name 			= Column(String(50), nullable=True)
 