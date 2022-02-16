from re import I
from flask_script import Command
from app import db
from configure import *
import json, logging

from app.users.models import *

from app.models.area import *
from app.models.group import *
from app.models.position import *
from app.models.mission import *
from app.models.orders import *
from app.models.product import *
from app.models.robot import *
from app.models.type_robot import *
from app.models.map import *
# from app.models.users import *
from app.models.robot_status import *
from app.models.step import *
from app.models.setting_charging_staging import *
from app.models.setting_collision_avoidance import *
from app.models.setting_distributor_data import *



class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        INITDB.ACTIVE = True
        init_db()
        db.create_all()
        logging.info('Migrate done')

def init_db():
    """ Initialize the database."""
    # logging.warning("----0")
    db.drop_all()
    # logging.warning("----1")
    db.create_all()
    create_user_roles()
    create_users()
    # logging.warning("----2")
    create_robots()
    # logging.warning("----3")

def create_user_roles():
    db.session.add(UserRole(name= "admin",      label = "Quản trị viên"))
    db.session.add(UserRole(name= "normal",    label = "Người dùng"))
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e.orig.args[1])

def create_users():
    """ Create users """

    # Adding roles
    admin = User(
        id = "admin",
        username = "admin", 		
        password="rostek",
        name= "rostek", 	
        email = "rostekcompany@gmail.com", 
        phone="+84986990169",	
        role_id= 1,
        active = True,
        description = "Des"
    )
    normal = User(
        id = "normal",
        username = "normal", 	
        password="123456", 
        name= "normal", 
        email = "rostekcompany@gmail.com",
        phone="+84986990169",	
        role_id= 2,
        active = True,
        description = "Des"
    )

    db.session.add(admin)
    db.session.add(normal)

    try:
        db.session.commit()
    except Exception as e:
        logging.error(e.orig.args[1])


def create_robots():
    missionDb  = Mission(
        name = "LOAD"
    )
    db.session.add(missionDb)
    db.session.flush()
    db.session.commit()

    productDb = Product(name = "Product1")
    db.session.add(productDb)
    db.session.flush()
    db.session.commit()

    groupDb  = Group(name = "Group1")
    db.session.add(groupDb)
    db.session.flush()
    db.session.commit()

    areaDb  = Area(
        name = "KV1"
    )
    db.session.add(areaDb)
    db.session.flush()
    db.session.commit()


    typeDb  = TypeRobot(
        type = "AMR"
    )
    db.session.add(typeDb)
    db.session.flush()
    db.session.commit()
    robotDb = Robot(
        name = "agv1",
        ip = '192.168.10.30',
        port = 9090,
        type_id = 1,
        group_id = 1,
        area_id = 1
    )
    db.session.add(robotDb)
    db.session.commit()

    mapDataDb = MapData()
    db.session.add(mapDataDb)
    db.session.commit()