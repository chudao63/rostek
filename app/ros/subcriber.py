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
		logging.info(f"payload--> {payload}")
		robot_id = payload["robot_id"]
		cmd = payload["cmd"]

		if cmd == 'load':
			print("load")
			position = {'y': 4, 'x':5, 'z': 7}
			orientation ={'y': 8, 'x': 11, 'z': 12, 'w': 4}
			Monitor.getInstance().robots[robot_id].send_message_to_agv(3,1,1,position,orientation) #gửi lệnh xuống agv, có 3 tham số, use poit_type
			# Monitor.getInstance().robots[robot_id].finish_load() #gửi lệnh xuống agv, có 3 tham số, use poit_type
			
		if cmd == 'unload':
			print("unload")
			position = {'y': 2, 'x':3, 'z': 0}
			orientation ={'y': 12, 'x': 3, 'z': 5, 'w': 1}
			Monitor.getInstance().robots[robot_id].send_message_to_agv(4,1,1,position,orientation) #gửi lệnh xuống agv, có 3 tham số, use poit_typequ
	
		
		if cmd == 'moving':
			print("moving")
			position = {'y': 14, 'x':25, 'z': 37}
			orientation ={'y': 81, 'x': 121, 'z': 172, 'w': 54}
			Monitor.getInstance().robots[robot_id].send_message_to_agv(1,1,1,position,orientation) #gửi lệnh xuống agv, có 3 tham số, use poit_type
		
	

			

	except Exception as e:
		logging.error(e)
Monitor.getInstance()