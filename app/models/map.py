from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, exc
from utils.dbmodel import DbBaseModel
from app import db
import sys, os, json, logging, yaml
from PIL import Image

class Map(db.Model, DbBaseModel):
	__tablename__ = "map"
	id 		= Column(String(50), primary_key=True, nullable=False)
	active  = Column(Boolean, default=False, nullable=False)

	
class MapData(db.Model, DbBaseModel):
	__tablename__ 	= "mapdata"
	id 		        = Column(Integer,  primary_key=True, autoincrement =True, index=True)
	active			= Column(Boolean, default = False, nullable = False)
	description 	= Column(String(200),  unique=False, nullable=True)

	@staticmethod
	def create_data_file(id):
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/{id}.yaml"
		data = {
			"points" : [],
			"paths" : [],
			"intersect" : [],
			"routes" : [],
		}
		with open(fileName, 'a+') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False)

	@staticmethod
	def delete_data_file(id):
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/{id}.yaml"
		if os.path.exists(fileName):
			os.remove(fileName)
			logging.info(f"Remove {id}.yaml")
		else:
			logging.error(f"The file {id}.yaml does not exist")

	@staticmethod
	def get_current_id():
		current = MapData.query.filter(MapData.active == True).first()
		if current:
			return current.id
		return 1

	@staticmethod
	def get_data():
		id = MapData.get_current_id()
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/{id}.yaml"
		with open(fileName) as file:
			data = yaml.load(file, Loader=yaml.FullLoader)
		return data

	@staticmethod
	def save_data(data):
		for point in data["points"]:
			if "rfid" not in point:
				point["rfid"] = ""
		data["points"] = list(reversed(data["points"]))
		data["paths"] = [i for n, i in enumerate(data["paths"]) if i not in data["paths"][n + 1:]]
		id = MapData.get_current_id()
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/{id}.yaml"
		with open(fileName, 'w') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False,  allow_unicode=True)
	
	@staticmethod
	def import_file(file, id):
		data = yaml.load(file, Loader=yaml.FullLoader)
		for point in data["points"]:
			if "rfid" not in point:
				point["rfid"] = ""
		data["points"] = list(reversed(data["points"]))
		# logging.info(f"Data ->> {data}")
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/{id}.yaml"
		with open(fileName, 'w') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False,  allow_unicode=True)
		
	@staticmethod
	def upload_image(file):
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/img/map.png"
		input_image = Image.open(file).convert('RGB')
		input_image.save(fileName, "PNG")
  
class Speed:
	@staticmethod
	def get_configure():
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/fms/map/data/speed.yaml"
		with open(fileName) as file:
			data = yaml.load(file, Loader=yaml.FullLoader)
		return data
	
	@staticmethod
	def save_configure(data):
		assert (type(data["speed"]) is int) or( type(data["speed"]) is float), "Speed phải là số nguyên hoặc số thực"
		assert (type(data["scale"]) is int) or( type(data["scale"]) is float), "Scale phải là số nguyên hoặc số thực"
		appPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		fileName = f"{appPath}/app/map/fms/data/speed.yaml"
		with open(fileName, 'w') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False,  allow_unicode=True)