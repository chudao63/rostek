from re import I
import coloredlogs

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from app.models.position import *
from app.models.area import *
from app.models.position import Position
from app.models.product import *
from utils.dbmodel import DbBaseModel


class Mission(db.Model, DbBaseModel):
    id       =  Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    name     =  Column(String(50),unique= True, nullable= False)
    start    =  Column(Integer, ForeignKey(Position.id), nullable= False)
    end      =  Column(Integer, ForeignKey(Position.id), nullable= False)
    product  =  Column(Integer, ForeignKey(Product.id), nullable= False)

