# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: "hoinv" - hoinv@rostek.com.vn

from flask_script import Command
from app.models.product import Product
from utils.vntime import VnTimestamp
import requests, random, logging, coloredlogs
import yaml, string
from app import db
from app.models.mission import Mission
from app.models.step import Step

class TestCommand(Command):
	""" Command for testing """
	def __init__(self):
		self.count = 1

	def test(self):
		pass
		#---- mission-step -----#
		# missions = Mission.query.all()
		# for mission in missions:
		# 	print(mission.id , "->>")
		# 	print(mission.steps)
		# # print(missions)
		# steps = Step.query.all()
		# # print(steps)
		# for step in steps:
		# 	print(step.id , "->>")
		# 	print(step.missions)
		# #append 
		# ms1 =  Mission.query.get(1)
		# st1 = Step.query.get(1)
		# # ms1.steps.pop(0)
		# ms1.steps.append(st1)
		# db.session.add(ms1)
		# db.session.commit()
		# ms1 =  Mission.query.get(1)
		# print(ms1.steps)

		#----- Join product - mission - step ---#
		# missionDb = db.session.query(Step).all()
		# productDb = db.session.query(Product).all()

		# findStep = db.session.query(
		# 	Step,
		# 	Mission,
		# 	Product
		# ).join(
		# 	Mission,
		# 	Step.id == Product.

		# )

	def run(self):
		db.session.begin_nested()
		try:
			self.test()
			db.session.commit()
		except AssertionError as error:
			logging.error(error)
		except Exception as e:
			db.session.rollback()
			logging.critical(e, exc_info=True)
		finally:
			db.session.commit()
			db.session.close()