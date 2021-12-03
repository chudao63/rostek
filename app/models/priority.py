from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from app import db
from utils.dbmodel import DbBaseModel

class Priority(db.Model, DbBaseModel):
    id          =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    level       =   Column(Integer, unique= True, nullable= False)
