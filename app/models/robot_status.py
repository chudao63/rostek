from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from app.fms.orders.consts import *
from app import db
from app.models.area import *
from app.models.type_robot import *
from utils.dbmodel import DbBaseModel
from utils.vntime import VnTimestamp

class RobotStatus(db.Model, DbBaseModel):
	__tablename__ = "robotstatus"
	id 				= Column(Integer, primary_key=True,nullable=False)
	robot_id 		= Column(Integer, ForeignKey('robot.id'), nullable=True)
	duration		= Column(Integer, default = 0,  nullable=False)
	status 		    = Column(String(50),  unique=False,  nullable=False) 
	pose 			= Column(String(500),  unique=False, nullable=True)
	info 			= Column(String(500),  unique=False, nullable=True)
	timestamp		= Column(Integer, default = 0,  nullable=False)

	def __init__(self, robot_id, duration, status, pose, info, timestamp):
		self.robot_id 	= robot_id 
		self.duration	= duration
		self.status 	= status 	
		self.pose     	= pose     
		self.info     	= info     			
		self.timestamp	= timestamp

	@staticmethod
	def get_lasteast_status(robotID):
		"""
		Lấy trạng thái cuối cùng của robot lưu trong hệ thống
		"""
		m = RobotStatus.query.order_by(RobotStatus.id.desc()).filter(RobotStatus.robot_id == robotID).first()
		if m:
			return {
				"status" : m.status,
				# "pose" : json.loads(m.pose),
				"pose" : m.pose,
				# "info" : json.loads(m.info),
				"info" : m.info,
			}
		return {
			"status" : 'STATUS_UNKNOWN',
			"pose" : {
				"x" : 0,
				"y" : 0,
				"theta" : 0
			},
			"info" : {
				"batery" : 100,
				"runningtime" : 100,
			}
		}

	@staticmethod
	def add_new_state(robotID, robotStatus, pose, info):
		"""add new state to db

		"""
		now = VnTimestamp.now()
		lateasteast_status = RobotStatus.query.order_by(RobotStatus.id.desc()).filter(RobotStatus.robot_id == robotID).first()
		# print(lateasteast_status)
		if lateasteast_status:
			duration = now - lateasteast_status.timestamp
		else:
			duration = 0
		m = RobotStatus(robotID, duration, robotStatus, pose, info, now)
		db.session.add(m)
		db.session.commit()
