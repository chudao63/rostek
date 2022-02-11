#!/usr/bin/python3


import time, schedule, coloredlogs, logging
from utils.scheduling import Actions
from flask_restful import reqparse
from flask import Flask

coloredlogs.install(
    level='INFO', 
    fmt = '[%(hostname)s] [%(pathname)s:%(lineno)s - %(funcName)s() ] %(asctime)s %(levelname)s %(message)s' 
)

def printer():
	logging.warning("HELLO")

def printer1():
	logging.warning("This is action printer 1")

def robot_runing_plan():
	logging.warning("robot runing")

app = Flask(__name__)

#http://127.0.0.1:5000/schedule/all
@app.route('/schedule/all')
def get_schedule():
	"""
	Get all action
	"""
	return Actions.get_instance().get_action()

#http://127.0.0.1:5000/schedule/add_printer?time=16:38&&action_id=1
@app.route('/schedule/add_printer')
def add_schedule():
	"""
	Add action
	"""
	message = "hello"
	parser = reqparse.RequestParser()
	parser.add_argument('time')
	parser.add_argument('action_id')
	args = parser.parse_args()

	Actions.get_instance().add_action({
		args["action_id"]: {
			"time" :  args["time"],
			"func" : printer
		}
	})
	return Actions.get_instance().get_action()

#http://127.0.0.1:5000/schedule/add_printer1?time=16:38&&action_id=2
@app.route('/schedule/add_printer1')
def add_schedule1():
	"""
	add action
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('time')
	parser.add_argument('action_id')
	args = parser.parse_args()

	Actions.get_instance().add_action({
		args["action_id"]: {
			"time" :  args["time"],
			"func" : robot_runing_plan
		}
	})
	return Actions.get_instance().get_action()

@app.route('/schedule/remove')
def remove_schedule():
	"""
	remove action
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('action_id')
	args = parser.parse_args()

	Actions.get_instance().remove_action(args["action_id"])
	return Actions.get_instance().get_action()

@app.route('/schedule/clear')
def clear_schedule():
	"""
	clear all action
	"""
	Actions.get_instance().clear_all_action()
	return Actions.get_instance().get_action()

if __name__ == "__main__":
	app.run()