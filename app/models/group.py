from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import ForeignKey
from app import db
from utils.dbmodel import DbBaseModel



class Group(db.Model, DbBaseModel):
    __tablename__ = 'group'
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name        = Column(String(50), unique= True, nullable= False)
    active      = Column(String(50),default= True ,nullable= True)
    # mission_id  = Column(Integer, ForeignKey('mission.id'), nullable= False)


