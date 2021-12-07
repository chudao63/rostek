from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from app import db
from utils.dbmodel import DbBaseModel


class TypeRobot(db.Model, DbBaseModel):
    __tablename__ = 'type_robot'
    id      =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    type    =   Column(String(50), unique= True ,nullable= False)

