from app import db
from utils.dbmodel import DbBaseModel
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, Integer, String, Boolean

class SettingChargingStaging(DbBaseModel, db.Model):
    __tablename__ = 'setting_charging_staging'
    id            = Column(Integer, autoincrement= True, primary_key= True, nullable= False)
    threshold     = Column(Float, nullable= True)
    auto_charging = Column(Boolean, default= True, nullable= True)
    auto_staging  = Column(Boolean, default= True, nullable= True)
    idle_time     = Column(Float, nullable= True)
    battery_for_charging = Column(Float, nullable= True)

