import enum

class PointTypeEnum(enum.Enum):
    MOVING 		= 1
    INTERSECT 	= 2
    LOAD 		= 3
    UNLOAD 		= 4
    ROTATE 		= 5
    CHARGE 		= 6

class RouteTypeEnum(enum.Enum):
    GOTO 		= 1
    GOBACK 	    = 2
