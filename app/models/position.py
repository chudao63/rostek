
from sqlalchemy.sql.schema import Column, ForeignKey, Index
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from utils.dbmodel import DbBaseModel



class Position(db.Model, DbBaseModel):
    __tablename__ = 'position'
    id           =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name         =   Column(String(50), nullable= False)
    X            =   Column(String(50), nullable= False)
    Y            =   Column(String(50), nullable= False)
    R            =   Column(Float,default=1, nullable= True)
    action       =   Column(String(50), nullable= False)








