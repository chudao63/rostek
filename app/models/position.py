
from os import cpu_count
from sqlalchemy.sql.schema import Column, ForeignKey, Index
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from utils.dbmodel import DbBaseModel
from sqlalchemy.orm import relation, relationship, backref


class Position(db.Model, DbBaseModel):
    __tablename__ = 'position'
    id           =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name         =   Column(String(50),unique= True, nullable= False)
    x            =   Column(Float, nullable= False)
    y            =   Column(Float, nullable= False)
    R            =   Column(Float,default=1, nullable= False)
    type         =   Column(String(50), nullable= False)
    map_data_id  =   Column(Integer, ForeignKey('mapdata.id'), nullable= False)
    mapDatas     =   relationship("MapData", backref='positions', lazy= False)









