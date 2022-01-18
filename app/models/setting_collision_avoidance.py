from app import db
from configure import FlaskConfigure
from utils.dbmodel import DbBaseModel
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer



class SettingCollisionAvoidance(DbBaseModel, db.Model):
    __tablename__   = 'setting_collision_avoidance'
    id                   = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    collision_avoidance = Column(Boolean, default= True, nullable= True)
