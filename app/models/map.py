from re import T
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import ForeignKey
from app import db
from utils.dbmodel import DbBaseModel



class Maps(db.Model, DbBaseModel):
    __tablename__ = 'maps'
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    file_name   = Column(String(50), unique= True,nullable= False)



