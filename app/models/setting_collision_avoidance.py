from app import db
from configure import FlaskConfigure
from utils.dbmodel import DbBaseModel
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean



class SettingCollisionAvoidance(DbBaseModel, db.Model):
    __tablename__   = 'setting_collision_advoidance'
    collision_advoidance = Column(Boolean, default= True, nullable= True)
