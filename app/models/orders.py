from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from app import db
from app.models.robot import *
from app.models.mission import *
from app.models.priority import *
from utils.dbmodel import DbBaseModel

class Order(db.Model, DbBaseModel):
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    start_time  = Column(String(50), nullable= False)
    end_time    = Column(String(50), nullable= False)
    status      = Column(String(50), nullable= False)
    robot       = Column(Integer, ForeignKey(Robot.id), nullable=False)
    mission     = Column(Integer, ForeignKey(Mission.id), nullable= False)
    priority    = Column(Integer, ForeignKey(Priority.id), nullable= False)
    active      = Column(String(50), nullable= False)
    note        = Column(String(300), nullable= False)
