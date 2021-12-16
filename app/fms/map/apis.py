import logging
import re
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.sqltypes import REAL
from app.models.map import Maps
from utils.apimodel import BaseApiPagination
from flask_restful import Resource, reqparse, request
import os, sys
from flask import send_from_directory
from app.models.map import Maps
from app import db

class MapsApi(BaseApiPagination):
    """
    URL: /map
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Maps, "/map")



class UploadMapApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imageName')

        args = parser.parse_args()

        if args['imageName']:
            datas = Maps.query.all()
            for data in datas:
                logging.error(data.file_name)
                if data.file_name == args['imageName']:
                    return "Namesake"

            map = Maps(file_name = args['imageName'])
            db.session.add(map)
            db.session.commit()
        

        if request.files:
            infile = request.files['file']
            appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
            fileName = f"{appPath}/upload_file/{str(args['imageName'])}.png"
            infile.save(fileName)
            return "Done!!!"

class DisplayMapApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imageName')
        args = parser.parse_args()
        logging.error(args)

        return send_from_directory(
            directory= f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/upload_file", filename= f"{args['imageName']}.png")



class DeleteImageApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        if args['id']:
            deleteImage = Maps.query.filter(Maps.id == args['id']).one()
            db.session.delete(deleteImage)
            db.session.commit()
            return "delete done"
        
