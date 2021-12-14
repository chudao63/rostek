from app import mqtt
import logging, json

from app.ros.consts import POINT_TYPE
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

		if cmd == 'load':
			print("load")
			Monitor.getInstance().robots[robot_id].send_message_to_agv(3,1,1) #gửi lệnh xuống agv, có 3 tham số, use poit_type
		
		if cmd == 'unload':
			print("unload")
			Monitor.getInstance().robots[robot_id].send_message_to_agv(4,1,1) #gửi lệnh xuống agv, có 3 tham số, use poit_type
		
		if cmd == 'moving':
			print("moving")
			Monitor.getInstance().robots[robot_id].send_message_to_agv(1,1,1) #gửi lệnh xuống agv, có 3 tham số, use poit_type
		
		# Monitor.getInstance().robots[robot_id].agv_status_printer(payload['pose'])

			

	except Exception as e:
		logging.error(e)
Monitor.getInstance()