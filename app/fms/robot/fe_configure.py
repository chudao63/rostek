
from utils.apimodel import BaseConfigureApi
from utils.yamlmodel import YamlReadWrite
import os, logging

class RobotConfigureApi(BaseConfigureApi, YamlReadWrite):
    """
    URL: /module/filter
    Lấy giá trị filter/post/path/delete cho frontend
    """
    def __init__(self):
        self.init_base_path(str(os.path.dirname(__file__)))