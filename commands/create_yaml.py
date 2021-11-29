from flask_script import Command
from app import db
from configure import *
import json, logging, yaml


class CreateYamlCommand(Command):
	""" Initialize the database."""
	def run(self):
		data = {
			"a" : 1
		}
		with open("commands/sample.yaml", 'w+') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False,  allow_unicode=True)
		logging.info('Migrate done')
