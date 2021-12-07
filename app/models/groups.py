from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import ForeignKey
from app import db
from utils.dbmodel import DbBaseModel



class Groups(db.Model, DbBaseModel):
    __tablename__ = 'groups'
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    group_name  = Column(String(50), unique= True, nullable= False)
    mission     = Column(Integer, ForeignKey('mission.id'), nullable= False)


