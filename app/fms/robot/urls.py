from app import api 
from .apis import RobotApi, RobotBaseApi, DeleteRobotApi
from .fe_configure import RobotConfigureApi


api.add_resource(
    RobotBaseApi,
    '/robot-base'
)

api.add_resource(
    RobotApi,
    '/robot'
)

api.add_resource(
    DeleteRobotApi,
    '/delete-robot'
)

api.add_resource(
    RobotConfigureApi, 
    '/robot/filter',      # replace robot to module name
    '/robot/post',        # replace robot to module name
    '/robot/patch',       # replace robot to module name
    '/robot/delete'       # replace robot to module name
)

