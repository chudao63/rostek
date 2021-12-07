from flask_script import Command
from app import db
from configure import *
import json, logging

from app.users.models import *

from app.models.area import *
from app.models.groups import *
from app.models.position import *
from app.models.mission import *
from app.models.orders import *
from app.models.product import *
from app.models.robot import *
from app.models.type_robot import *
# from app.models.users import *



class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        INITDB.ACTIVE = True
        init_db()
        logging.info('Migrate done')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_user_roles()
    create_users()


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
