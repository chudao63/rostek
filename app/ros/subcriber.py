from app import mqtt
import logging, json
from .realtime import RobotRuning
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
		robots = Robot.query.all()
		for robot in robots:
			self.robots[robot.id] = RobotRuning(robot.id, robot.ip, robot.port)

		if Monitor.__instance != None:
			raise Exception("Do not call __init__(). Monitor is a singleton!")
		else:
			Monitor.__instance = self

mqtt.subscribe("/agv/cmd")

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
		robot_id = payload["robot_id"]
		cmd = payload["cmd"]
		Monitor.getInstance().robots[robot_id].
	except Exception as e:
		logging.error(e)

Monitor.getInstance()