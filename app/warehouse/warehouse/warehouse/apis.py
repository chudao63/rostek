
from utils.apimodel import ApiCommon
from app.models.warehouse import Warehouse
import os, logging

class WarehouseApi(ApiCommon):
    """
    URL: /warehouse
    """
    def __init__(self):
        ApiCommon.__init__(self, Warehouse, "/warehouse")