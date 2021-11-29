from sqlalchemy import Column, Integer, String
from utils.dbmodel import DbBaseModel
from app import db

class BinSize(db.Model, DbBaseModel):
	__tablename__ = "binsize"
	id 				= Column(Integer, primary_key=True, autoincrement =True, index=True)
	name 			= Column(String(100),  unique=True)
