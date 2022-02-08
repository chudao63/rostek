import logging
from app.models.map import Map
from utils.apimodel import BaseApiPagination, ApiBase
from flask_restful import Resource, reqparse, request
import os, sys
from flask import send_from_directory
from app.models.map import Map





class DownloadLogFileApi(Resource):
	"""
	Lấy dữ liệu của file log
	URL: '/display'
	Param: 'imageName'
	"""
	def get(self):
		return send_from_directory(
			directory= f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/logs", filename= f"user_log.log", as_attachment = True)

