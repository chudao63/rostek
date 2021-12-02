from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from app import db
from app.models.mission import *
from utils.dbmodel import DbBaseModel


class Groups(db.Model, DbBaseModel):
    id          = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    group_name  = Column(db.String(50), unique= True, nullable= False)
    mission     = Column(Integer, ForeignKey(Mission.id), nullable= False)

