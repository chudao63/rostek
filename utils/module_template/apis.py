
from utils.apimodel import ApiCommon
from app.models.example import Example
import os, logging

class ExampleApi(ApiCommon):
    """
    URL: /example
    """
    def __init__(self):
        ApiCommon.__init__(self, Example, "/example")