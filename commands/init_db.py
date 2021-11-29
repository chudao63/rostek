from flask_script import Command
from app import db
from configure import *
import json, logging
from app.models.warehouse import *
from app.models.bin_size import *

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        INITDB.ACTIVE = True
        init_db()
        logging.info('Migrate done')

def init_db():
    """ Initialize the database."""
    # db.drop_all()
    db.create_all()
