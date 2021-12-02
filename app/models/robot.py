
from humanfriendly.compat import basestring
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from app.models.area import *
from app.models.type_robot import *
from app.models.groups import *
from utils.dbmodel import DbBaseModel




class Robot(db.Model, DbBaseModel):
    id          =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name        =   Column(String(50), unique= True, nullable= False)
    battery     =   Column(Float, nullable= False)
    ip_adress   =   Column(String(50), nullable= False)
    status      =   Column(String(10), nullable= False)
    area        =   Column(Integer, ForeignKey(Area.id), nullable= False)
    type        =   Column(Integer, ForeignKey(TypeRobot.id), nullable= False )
    group       =   Column(Integer, ForeignKey(Groups.id), nullable= True)

