from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
import coloredlogs, jwt
from flask_socketio import SocketIO
import eventlet
from flask_mqtt import Mqtt
import logging, os
from configure import *

"""
CONFIGURE LOG
"""
coloredlogs.install(level='INFO', fmt = '[%(hostname)s] [%(pathname)s:%(lineno)s - %(funcName)s() ] %(asctime)s %(levelname)s %(message)s' )
# homepath = os.path.expanduser('~')
# logging.basicConfig(
#     format  = '%(asctime)s - %(filename)s:%(lineno)s - %(funcName)10s() - %(levelname)s - %(message)s',
#     filename= f'{homepath}/agv-server.log',
#     level   = logging.INFO
# )

eventlet.monkey_patch()
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'app')
print(TEMPLATE_PATH)
app = Flask(__name__, template_folder=TEMPLATE_PATH)

CORS(app)


"""
CONFIGURE SQLALCHEMY
"""
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{MysqlConfigure.USER}:{MysqlConfigure.PASSWORD}@{MysqlConfigure.HOST}/{MysqlConfigure.DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 50

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app=app)

"""
CONFIGURE MQTT
"""
app.config['MQTT_BROKER_URL'] = MqttConfigure.MQTT_BROKER_URL
app.config['MQTT_BROKER_PORT'] = MqttConfigure.MQTT_BROKER_PORT
app.config['MQTT_USERNAME'] = MqttConfigure.MQTT_USERNAME
app.config['MQTT_PASSWORD'] = MqttConfigure.MQTT_PASSWORD
app.config['MQTT_KEEPALIVE'] = MqttConfigure.MQTT_KEEPALIVE
app.config['MQTT_TLS_ENABLED'] = MqttConfigure.MQTT_TLS_ENABLED

api = Api(app, prefix='/api/v1')
app.config['SECRET_KEY'] = '123456'
socketio = SocketIO(app)

try:
    mqtt = Mqtt(app)
except:
    logging.error("Can't connect to MQTT Broker")

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['TEMPLATES_AUTO_RELOAD'] = True
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

