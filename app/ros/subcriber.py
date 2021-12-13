from app import mqtt
import logging, json
from .realtime import RobotRuning
from configure import ROS_BRIDGE
from app.models.robot import Robot

class Monitor:
	"""
	Single turn Class for saving current oee data

	"""
	__instance = None
	@staticmethod
	def getInstance():
		if Monitor.__instance == None:
			Monitor()
		return Monitor.__instance

	def __init__(self):
		self.robots = {}
		if Monitor.__instance != None:
			raise Exception("Do not call __init__(). Monitor is a singleton!")
		else:
			Monitor.__instance = self

if ROS_BRIDGE.ACTIVE:
	robots = Robot.query.all()
	for robot in robots:
		Monitor.getInstance().robots[robot.id] = RobotRuning(robot.id, robot.ip, robot.port)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    pass

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	logging.warning("on message")
	try:
		topic=message.topic
		payload=json.loads(message.payload.decode())
		logging.info(payload)

	except Exception as e:
		logging.error(e)

