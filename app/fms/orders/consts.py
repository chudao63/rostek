import enum
from operator import le

class ORDER_STATUS(enum.Enum):
    FINISH = 0
    WAITTING = 1
    RUNNING = 2


class ORDER_ACTIVE(enum.Enum):
    TRUE = 1
    FALSE = 0
    

class ORDER_PRIORITY(enum.Enum):
    LEVEL_1  = 1
    LEVEL_2  = 2
    LEVEL_3  = 3
    LEVEL_4  = 4    
    LEVEL_5  = 5

class TYPE_JOB(enum.Enum):
    LIFT = 1
    DRAG = 2 
    