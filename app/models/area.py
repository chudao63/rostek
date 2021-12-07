from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from app import db
from utils.dbmodel import DbBaseModel



class Area(db.Model, DbBaseModel):
    __tablename__ = 'area'
    id      =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name    =   Column(String(50), unique= True, nullable= False)

