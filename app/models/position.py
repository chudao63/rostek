
from os import cpu_count
from sqlalchemy.sql.schema import Column, ForeignKey, Index
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from utils.dbmodel import DbBaseModel
from sqlalchemy.orm import relation, relationship, backref



position_mapdata = db.Table('position_mapdata',
    Column('position_id', Integer, ForeignKey('position.id'), primary_key= True),
    Column('map_data_id', Integer, ForeignKey('mapdata.id'), primary_key= True)
)

class Position(db.Model, DbBaseModel):
    __tablename__ = 'position'
    id           =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name         =   Column(String(50), nullable= False)
    X            =   Column(Float, nullable= False)
    Y            =   Column(Float, nullable= False)
    R            =   Column(Float,default=1, nullable= False)
    action       =   Column(String(50), nullable= False)
    mapDatas    =   relationship("MapData",secondary=position_mapdata, lazy='subquery', backref=backref('positions', lazy=False))









