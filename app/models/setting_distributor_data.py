from ast import Str
from asyncio import FastChildWatcher
from email.message import EmailMessage
import imp
from shutil import _ntuple_diskusage
from app import db
from utils.dbmodel import DbBaseModel
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, String, Integer


class SettingDistributorData(DbBaseModel, db.Model):
    __tablename__ = 'setting_distributor_data'
    id            = Column(Integer, autoincrement= True, primary_key= True, nullable= False)
    address       = Column(String(100), nullable= False)    
    city          = Column(String(100), nullable= False)
    country       = Column(String(100), nullable= False)
    email         = Column(String(100), nullable= False)
    name          = Column(String(100), nullable= False)
    phone         = Column(String(100), nullable= False)

