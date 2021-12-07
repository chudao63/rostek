
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db

from utils.dbmodel import DbBaseModel


class Mission(db.Model, DbBaseModel):
    __tablename__ = 'mission'
    id       =  Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name     =  Column(String(50),unique= True, nullable= False)
    start    =  Column(Integer, ForeignKey('position.id'), nullable= False)
    end      =  Column(Integer, ForeignKey('position.id'), nullable= False)
    type_job =  Column(Integer, nullable=False)
    product  =  Column(Integer, ForeignKey('product.id'), nullable= False)

