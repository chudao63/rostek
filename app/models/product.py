from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from app import db
from utils.dbmodel import DbBaseModel



class Product(db.Model, DbBaseModel):
    __tablename__ = 'product'
    id     =    Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name   =    Column(String(50),unique= True, nullable= False)
