from sqlalchemy.sql.schema import Column, Index
from sqlalchemy.sql.sqltypes import Float, Integer, String
from app import db
from utils.dbmodel import DbBaseModel


class Location(db.Model, DbBaseModel):
    id           =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    startX       =   Column(Float, nullable= False )
    startY       =   Column(Float, nullable= False)
    endX         =   Column(Float, nullable= False )
    endY         =   Column(Float, nullable= False)
    ban_kinh_R   =   Column(Float, nullable= False)
