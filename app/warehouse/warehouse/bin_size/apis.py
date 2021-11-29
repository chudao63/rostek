
from utils.apimodel import ApiCommon
from app.models.bin_size import BinSize
import os, logging

class BinSizeApi(ApiCommon):
    """
    URL: /bin_size
    """
    def __init__(self):
        ApiCommon.__init__(self, BinSize, "/bin_size")