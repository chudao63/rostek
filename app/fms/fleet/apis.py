import re
from flask_restful import Resource, request, reqparse
from app.models.robot import *
from sqlalchemy import and_
from utils.apimodel import BaseApiPagination
from app.models.robot import Robot

class FleetApi(Resource):
    def __init__(self):
        BaseApiPagination.__init__(self, Robot, "/Fleet")