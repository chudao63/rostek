import re
from sqlalchemy.sql.sqltypes import REAL
from utils.apimodel import BaseApiPagination
from app.models.priority import Priority

class PriorityApi(BaseApiPagination):
    """
    URL: /location
    """
    def __init__(self):
        BaseApiPagination.__init__(self, Priority, "/priority")
