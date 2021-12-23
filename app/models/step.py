
from typing import Collection
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from app.models.mission import Mission
from utils.dbmodel import DbBaseModel
from sqlalchemy.orm import relation, relationship



class Step(db.Model, DbBaseModel):
    __tablename__  = 'step_table'
    id             =  Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    start_point    =  Column(Integer, ForeignKey('position.id'), nullable= False)
    end_point      =  Column(Integer, ForeignKey('position.id'), nullable= False)





