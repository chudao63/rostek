from app import app
from configure import *

"""
IMPORT URL FROM SOFTWARE
"""

from app.users.urls import *
from app.update.urls import *
from app.fms.urls import *
# from app.ros.subcriber import *
from app import socketio
# import write_log
# import tailer

# write_log.setup_logger(name = 'user_log', log_file= 'logs/user_log.log', message= tailer.tail(open('logs/user_log.log'), 1)[1])

if __name__ == "__main__":
    if MqttConfigure.ACTIVE:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=FlaskConfigure.DEBUG)
    else:
        socketio.run(app, host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=FlaskConfigure.DEBUG)
    # app.run(host=FlaskConfigure.HOST, port=FlaskConfigure.PORT, use_reloader=False , debug=False)