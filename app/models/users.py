# from os import access

# from sqlalchemy.sql.expression import false, null
# from app import db
# from app.models.area import *

# from sqlalchemy import Column, String, Integer, ForeignKey, Float
# from utils.dbmodel import DbBaseModel



# class Users(db.Model, DbBaseModel):
#     id          =   Column(Integer, primary_key= True, autoincrement= True, nullable= False)
#     user_name    =   Column(String(50), nullable= False)
#     access_level =   Column(String(50), nullable= False)
#     location    =   Column(Integer, ForeignKey(Area.id), nullable= False)
#     password    =   Column(String(50), nullable= False)
#     name        =   Column(String(50), nullable= False)
#     email       =   Column(String(50), nullable= False)
#     telephone   =   Column(String(20), nullable= False)

# db.create_all()
