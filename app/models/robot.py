from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String,Boolean
from app.fms.orders.consts import *
from app import db
from app.models.area import *
from app.models.type_robot import *
from utils.dbmodel import DbBaseModel

class Robot(db.Model, DbBaseModel):
    __tablename__ = 'robot'
    id          =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name        =   Column(String(50), unique= True, nullable= False)
    ip          =   Column(String(50), unique= True,nullable= False)
    port        =   Column(Integer, nullable= False)
    active      =   Column(Boolean, default =True, nullable=False)
    area_id        =   Column(Integer, ForeignKey('area.id'), nullable= True)
    type_id        =   Column(Integer, ForeignKey('type_robot.id'), nullable= False )
    group_id       =   Column(Integer, ForeignKey('group.id'), nullable= True)


