from app import app
from configure import *

"""
IMPORT URL FROM SOFTWARE
"""

from app.users.urls import *
from app.update.urls import *
from app.fms.urls import *
from app.ros.subcriber import *
from app import socketio




if __name__ == "__main__":
    if MqttConfigure.ACTIVE:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=FlaskConfigure.DEBUG)
    else:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=FlaskConfigure.DEBUG)
    # app.run(host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=False)