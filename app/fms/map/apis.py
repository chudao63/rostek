import re
from sqlalchemy.sql.sqltypes import REAL
from app.models.map import Maps
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse, request
import os, sys
from flask import send_from_directory
from flask import Flask
from app import app


class MapsApi(BaseApiPagination):
    """
    URL: /map
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Maps, "/map")



class UploadMapApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileName')

        args = parser.parse_args()

        if request.files:
            infile = request.files['file']
            appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
            fileName = f"{appPath}/upload_file/{str(args['fileName'])}.png"
            infile.save(fileName)
            return "Done!!!"
