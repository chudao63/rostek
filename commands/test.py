# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: "hoinv" - hoinv@rostek.com.vn

from flask_script import Command
from utils.vntime import VnTimestamp
import requests, random, logging, coloredlogs
import yaml, string

class TestCommand(Command):
	""" Command for testing """
	def __init__(self):
		self.count = 1

	def test(self):
		print("testing")

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
			return create_response_message(str(e),409)
		finally:
			db.session.commit()
			db.session.close()