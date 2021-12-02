from utils.autoimport import import_all_urls
import logging
# from app.warehouse.warehouse.urls import *
rootdir = 'app/fms'
# logging.info(rootdir)
import_all_urls(rootdir)