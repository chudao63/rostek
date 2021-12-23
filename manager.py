
"""This file sets up a command line manager.
Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for a list of runserver options.
"""

from flask_script import Manager, Command

from app import app
from commands import *

manager = Manager(app)
manager.add_command('init_db', InitDbCommand)
manager.add_command('test', TestCommand)
manager.add_command('create_yaml', CreateYamlCommand)

if __name__ == "__main__":
    # python manage.py                      # shows available commands
    # python manage.py runserver --help     # shows available runserver options
    manager.run()