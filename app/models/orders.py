import re
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import  Integer, Boolean
from sqlalchemy import String
from app import db
from utils.dbmodel import DbBaseModel
from app.fms.orders.consts import *

class Order(db.Model, DbBaseModel):
    __tablename__ = 'order'
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    start_time  = Column(String(50), nullable= False)
    end_time    = Column(String(50), nullable= False)
    status      = Column(Integer, default=1,  unique=False,  nullable=False)
    robot_id    = Column(Integer, ForeignKey('robot.id'), nullable=True)
    mission_id  = Column(Integer, ForeignKey('mission.id'), nullable= False)
    priority    = Column(Integer, default=1,nullable= False)
    active      = Column(Boolean, default = 1, nullable=False)
    note        = Column(String(300), nullable= True)
    robot       = relationship("Robot", backref= "order", lazy= True) #***#
    mission     = relationship("Mission", backref= "order", lazy= True)

