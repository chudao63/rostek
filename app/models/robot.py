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
    battery     =   Column(Float, nullable= False)
    ip          =   Column(String(50), unique= True,nullable= False)
    port        =   Column(Integer, nullable= False)
    active      =   Column(Boolean, default = ORDER_ACTIVE.TRUE.name, nullable=False)
    area        =   Column(Integer, ForeignKey('area.id'), nullable= False)
    type        =   Column(Integer, ForeignKey('type_robot.id'), nullable= False )
    group       =   Column(Integer, ForeignKey('groups.id'), nullable= True)


