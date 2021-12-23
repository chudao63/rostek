
from sqlalchemy.orm import relation, relationship, backref
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db

from utils.dbmodel import DbBaseModel

mission_step = db.Table('mission_step',
    Column('mission_id', Integer, ForeignKey('mission.id'), primary_key= True),
    Column('step_id', Integer, ForeignKey('step_table.id'), primary_key= True)
)

class Mission(db.Model, DbBaseModel):
    __tablename__ = 'mission'
    id       =  Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name     =  Column(String(50),unique= True, nullable= False)
    steps = relationship("Step",secondary=mission_step, lazy='subquery', backref=backref('missions', lazy=False))

