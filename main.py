from app import app, socketio
from configure import *
from flask import send_from_directory

"""
IMPORT URL FROM SOFTWARE
"""
from app.users.urls import *
from app.update.urls import *
from app.fms.urls import *


if __name__ == "__main__":
    if MqttConfigure.ACTIVE:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=True , debug=FlaskConfigure.DEBUG)
    else:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=True , debug=FlaskConfigure.DEBUG)