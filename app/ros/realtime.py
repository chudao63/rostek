import logging, json, roslibpy, time

from sqlalchemy.sql.functions import count
from app.models.robot_status import RobotStatus
from .subcriber import mqtt
from configure import MqttConfigure
from squaternion import Quaternion
from configure import *
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from utils.vntime import VnTimestamp
from .consts import *

class RobotRuning:
	def __init__(self, robotId, ip, port):
		self.engine 					= engine.create_engine(f"mysql://{MysqlConfigure.USER}:{MysqlConfigure.PASSWORD}@{MysqlConfigure.HOST}/{MysqlConfigure.DATABASE}")
		self.Session 					= sessionmaker(bind=self.engine)
		self.robotId 					= robotId
		lasteastStatus 					= RobotStatus.get_lasteast_status(robotId)
		self.__robotStatus				= lasteastStatus["status"]
		self.pose 						= lasteastStatus["pose"]
		self.info 						= lasteastStatus["info"]
		self.__robotState 				= 0
		self.count						= 0
		self.number 					= 0
		self.mqtt_count 				= 0
		self.error 						= False
		self.time 						= 0
		self.agvWayPointCountFeedback 	= 0
		self.agvWayPointLengthFeedback  = 0
		self.ip 						= ip
		self.port 						= port
		self.init_ros_bridge()
		self.latestTimeSendOrder 		= VnTimestamp.now() # Lần cuối nhận lệnh gửi Order xuống AGV
		self.latestChangeState  		= VnTimestamp.now() # Lần cuốit thay đổi trạng thái
		self.count = 0

	def __repr__(self):
		return json.dumps(self.as_dict)

	@property
	def as_dict(self):
		return {
			"robot_id" 		: self.robotId,
			"status"	    : self.__robotStatus,
			"pose"          : self.pose,
			"info"			: self.info
		}

	def mqtt_publish(self):
		"""
		GỬI DỮ LIỆU TỚI FRONTEND
		"""
		pose = self.pose.copy()
		theta = pose.pop("theta")
		pose["θ"] = theta
		data = {
			"robot_id" 		: self.robotId,
			"status"	    : self.__robotStatus,
			"pose"          : pose,
			"info"			: self.info
		}
		mqtt.publish(MqttConfigure.FRONTEND_TOPIC, json.dumps(data))
		self.mqtt_count += 1
		print(f"Pub to frontend -> {self.mqtt_count}")


	def update(self, data):
		"""
		UPDATE DỮ LIỆU ROBOT {"status" : "LOADING", "pose" : {"x": 0, "y": 0, "theta": 0}}
		"""
		self.count += 1
		if 'pose' in data:
			self.pose = data['pose']
		if 'info' in data:
			self.info = data['info']
		if 'status' in data:
			self.robotStatus = data['status']
		if self.count == MqttConfigure.AGV_COUNT_MESSAGE:
			self.mqtt_publish()
			self.count = 0
		if 'state' in data:
			self.robotState = data['state']
		if 'conveyor_status' in data:
			self.agv_order = data['conveyor_status']

	@property
	def robotStatus(self):
		return self.__robotStatus  
	
	@robotStatus.setter
	def robotStatus(self, robotStatus):
		if robotStatus != self.__robotStatus:
			RobotStatus.add_new_state(self.robotId, robotStatus,self.pose, self.info)
			self.__robotStatus = robotStatus
			self.mqtt_publish()
			# logging.info(f"Saving {self.robotId} -> status = {robotStatus}")

	@property
	def robotState(self):
		return self.__robotState  
	
	@robotState.setter
	def robotState(self, robotState):
		"""
		Check thay đổi trạng thái của robot
		"""
		if robotState != self.__robotState:
			self.latestChangeState   = VnTimestamp.now()
			self.__robotState = robotState
			if robotState == 1 or robotState == 2:
				logging.warning("------- LOAD ORDER -------")
				# self.load_test()
			elif robotState == 8:
				logging.warning("------- UNLOAD ORDER -------")
			elif robotState == 7 or robotState == 11 or robotState == 12:
				self.error = True


	def reinit_ros_bridge(self):
		"""
		Kết nối lại đến AGV
		"""
		self.rosClient.close()
		time.sleep(2)
		self.rosClient.connect()
		time.sleep(3)

	def ros_subcribe(self):
		"""
		Nếu kết nối được tới AGV thì khởi tạo các Subscriber
		"""
		try:
			if self.rosClient.is_connected :
				self.agvStatus = roslibpy.Topic(self.rosClient, '/agv_status', 'geometry_msgs/PoseStamped')
				self.agvWayPoint = roslibpy.Topic(self.rosClient, '/agv_waypoints', 'geometry_msgs/PoseStamped')
				self.agvOrderCommand = roslibpy.Topic(self.rosClient, '/order_command', 'std_msgs/String')
				self.agvWayPoint.subscribe(self.agv_control_printer)
				self.agvStatus.subscribe(self.agv_status_printer)
				self.agvPose = roslibpy.Topic(self.rosClient, '/amcl_pose', 'geometry_msgs/PoseWithCovarianceStamped')
				self.agvPose.subscribe(self.pose_message_handler)
				#topic feedback
				self.agvWaypointFeedback = roslibpy.Topic(self.rosClient, '/agv_fb_waypoints', 'geometry_msgs/PoseStamped')
				self.agvWaypointFeedback.subscribe(self.handle_waypoint_feedback)
				logging.info(f"Init ROSBRIDGE {self.robotId} sucessfull")
				mqtt.publish('/messeger_rosbridge', f"Init ROSBRIDGE {self.robotId} sucessfull")
		except Exception as e:
			logging.error(str(e))

	def init_ros_bridge(self):
		"""
		Khởi tạo kết nối tới AGV
		"""
		try:
			self.rosClient = roslibpy.Ros(host=self.ip , port=self.port)
			self.rosClient.factory.set_max_delay(10)
			self.rosClient.run()
			# roslibpy.set_rosapi_timeout(10)
			self.rosClient.on_ready(lambda: print('Is ROS connected?', self.rosClient.is_connected))
			self.ros_subcribe()
		except:
			logging.error(f"Init ROSBRIDGE {self.robotId} FALSE")
			mqtt.publish('/messeger_rosbridge', f"Init ROSBRIDGE {self.robotId} false")
	
	def handle_waypoint_feedback(self,message):
		"""
  		Lắng nghe feedback từ agv sau khi gửi command
    	"""
		logging.error(f" <<-- {message}")
		self.agvWayPointCountFeedback += 1
		if self.agvWayPointCountFeedback == self.agvWayPointLengthFeedback:
			if self.agvWayPointCurrentTypeFeedback == 3:
				self.finish_load()
			elif self.agvWayPointCurrentTypeFeedback==4:
				self.finish_unload()
   
	def pose_message_handler(self,message):
		"""
		Lắng nghe thay đổi vị trí của robot
		"""
		# if self.count <50:
		# 	self.count = self.count +1
		# 	return 
		print("->>",message)
		pose = message['pose']['pose']['position']
		pose.pop('z')
		orientation = message['pose']['pose']['orientation']
		q = Quaternion(w=orientation['w'], x=orientation['x'], y=orientation['y'], z=orientation['z'])
		theta = q.to_euler(degrees=True)
		pose["theta"] = theta[2]
		payload = {
			"robot_id" : self.robotId,
			"pose" : {
				"x" : round(pose['x']*1000),
				"y" : round(pose['y']*1000),
				"theta" : pose['theta'],
			}
		}
		self.update(payload)

	def agv_status_printer(self,message):
		"""
		Lắng nghe thay đổi trạng thái của robot
		"""
		# print(message)
		# print("->")
		frame_id = json.loads(message['header']['frame_id'])
		pose = message['pose']['position']
		pose.pop('z')
		orientation = message['pose']['orientation']
		q = Quaternion(w=orientation['w'], x=orientation['x'], y=orientation['y'], z=orientation['z'])
		theta = q.to_euler(degrees=True)
		pose["theta"] = theta[2]
		payload = {
			"robot_id" : self.robotId,
			"status" : AGV_STATUS[frame_id['status']],
			"state" : frame_id['state'],
			"pose" : {
				"x" : round(pose['x']*1000),
				"y" : round(pose['y']*1000),
				"theta" : pose['theta'],
			},
			"info" : {
				"runningtime" : frame_id["runningtime"],
				"batery" : frame_id["battery"]
			},
			"conveyor_status" : frame_id["conveyor_status"]
			# "conveyor_status" : 1

		}
		self.update(payload)


	def agv_control_printer(self, message):
		"""
		In các bản tin điều khiển
		"""
		# print("Control message ->")
		print(message)
		pass

	def send_message_to_agv(self,point_type, station, floor, positon, orientation):
		"""
		Tạo bản tin chứa data cần gửi xuống AGV
		"""
		#2 chỗ cần check dumps message và dumps frame_id
		logging.info("create command to agv")
		frame_id = {
			'point_type' : point_type,
			'station_code' : station,
			'task_type' : 0,
			'plc_task': floor
		}
		# logging.info(frame_id)
		message = {
			'header': {'stamp': {'secs': 0, 'nsecs': 0}, 
			'frame_id': json.dumps(frame_id), 
			'seq': 1}, 
			'pose': {'position': positon,
			'orientation': orientation}
		}
		if self.agvWayPoint:
			self.agvWayPoint.publish(message)
			# logging.warning(message)
		else:
			logging.error("AGV chua ket noi voi server")

		
	def finish_load(self):
		"""
  		ROSBRIDGE => Gửi xuống AGV khi kết thúc load order
    	"""
		logging.info("Sending Finish LOAD Order")
		self.agvOrderCommand.publish({'data':'LOAD'})
	
	def finish_unload(self):
		"""
		ROSBRIDGE => Gửi xuống AGV khi kết thúc Unload order
		"""
		logging.info("Sending Finish UNLOAD Order")
		self.agvOrderCommand.publish({'data':'UNLOAD'})

