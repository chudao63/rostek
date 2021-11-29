import logging, json
from utils.apimodel import ApiBase
from flask_restful import request
from flask_jwt_extended import jwt_required
from app import mqtt
from utils.vntime import VnTimestamp
import random
from .const import POINT_DATA
import random


class FrontendTestApi(ApiBase):
    """URL: /agv1

    """
    def get(self):
        point = random.randint(0, 28)
        data = {
            "robot_id": request.path[1:],
            "status": "MOVING",
            "point": f"Point{point}",
            "path": f"Point{point}-Point{point+1}",
            "battery": random.randint(50, 100),
            "runningtime": random.randint(1000, 2000),
            "time" : random.randint(5, 15),
        }
        mqtt.publish("/agv/realtime", json.dumps(data))
        return f"{data['robot_id']} move from {data['path']}"

class BackendTestApi(ApiBase):
    """URL:

    """
    def get(self):
        data = self.request_parser(["uid","status","point","route"], [])
        if data["status"] == 'i':
                status = "IDLE"
        elif data["status"] == 'e':
            status = "GENERAL_ERROR"
        elif data["status"] == 'm':
            status = "MOVING"
        elif data["status"] == 'h':
            status = "HOME"
        elif data["status"] == 'h1':
            status = "HOME_TRANSPORT"
        print(data)
        data = {
            "uid" : int(data["uid"]),
            "rfid" : data["point"]*3,
            "route_id" : int(data["route"]),
            "status" : status,
            "command" : "",
            "battery" : random.randint(50, 100),
            "runningtime" : random.randint(1000, 10000)
        }
        logging.info(f"->>>>> {data}")
        mqtt.publish("/agv_monitor", json.dumps(data))
        return f"AGV {data['uid']} {status} DONE!"

class NotifyApi(ApiBase):
    """URL: /notify

    """
    def get(self):
        if "/notify_sucess" in request.path:
            data = {
                "notify" : f"Sucess {VnTimestamp.now()}",
                "type" : "success"
            }
        if "/notify_error" in request.path:
            data = {
                "notify" : f"Error {VnTimestamp.now()}",
                "type" : "error"
            }
        mqtt.publish("/agv/notify", json.dumps(data))
        return f"Done"

class FrontendIntersectApi(ApiBase):
    """URL: /intersect_0; /intersect_empty

    """
    def get(self):
        if "/intersect_0" in request.path:
            data = {"name": "Giao l\u1ed9 1", "list_path": ["Point9-Point10", "Point19-Point10"], "current_agv": "agv2", "waiting_agv": []}
        elif "/intersect_1" in request.path:
            data = {"name": "Giao l\u1ed9 1", "list_path": ["Point9-Point10", "Point19-Point10"], "current_agv": "agv2", "waiting_agv": [
                {"robot_id": "agv1", "point": "Point9", "path": "Point9-Point10", "route_id": 4, "status": "MOVING"}
            ]}
        elif "/intersect_2" in request.path:
            data = {"name": "Giao l\u1ed9 1", "list_path": ["Point9-Point10", "Point19-Point10"], "current_agv": "agv2", "waiting_agv": [
                {"robot_id": "agv1", "point": "Point9", "path": "Point9-Point10", "route_id": 4, "status": "MOVING"},
                {"robot_id": "agv3", "point": "Point9", "path": "Point9-Point10", "route_id": 4, "status": "MOVING"}
            ]}
        elif "/intersect_3" in request.path:
            data = {"name": "Giao l\u1ed9 1", "list_path": ["Point9-Point10", "Point19-Point10"], "current_agv": "agv2", "waiting_agv": [
                {"robot_id": "agv1", "point": "Point9", "path": "Point9-Point10", "route_id": 4, "status": "MOVING"},
                {"robot_id": "agv3", "point": "Point9", "path": "Point9-Point10", "route_id": 4, "status": "MOVING"},
                {"robot_id": "agv4", "point": "Point9", "path": "Point19-Point10", "route_id": 6, "status": "MOVING"}
            ]}
        mqtt.publish("/agv/intersect", json.dumps(data))