from utils.autoimport import import_all_urls
import logging

rootdir = 'app/fms'
logging.error(import_all_urls(rootdir))
import_all_urls(rootdir)