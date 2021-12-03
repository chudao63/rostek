from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Enum, Integer, Boolean
from app import db
from app.models.robot import *
from app.models.mission import *
from app.models.priority import *
from utils.dbmodel import DbBaseModel
from app.fms.orders.consts import *

class Order(db.Model, DbBaseModel):
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    start_time  = Column(String(50), nullable= False)
    end_time    = Column(String(50), nullable= False)
    status      = Column(Integer, default=OrderStatus.Released.name,  unique=False,  nullable=False)
    robot       = Column(Integer, ForeignKey(Robot.id), nullable=False)
    mission     = Column(Integer, ForeignKey(Mission.id), nullable= False)
    priority    = Column(Integer, ForeignKey(Priority.id), nullable= False)
    active      = Column(Boolean, default = True, nullable=False)
    note        = Column(String(300), nullable= False)

