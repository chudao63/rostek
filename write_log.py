from asyncio.log import logger
import json
import logging
from app import mqtt
from configure import MqttConfigure

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, message, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    """
    Lưu lại log vào file log đồng thời gửi 1 bản tin lên front end qua mqtt
    """

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.info(message)
    mqtt.publish("/system/log", message)



# setup_logger(name = 'user_log', log_file= 'logs/user_log.log', message= "hello")


# logger = logging.getLogger()
# handler = logging.FileHandler('logs/user_log.log')
# logger.addHandler(handler)
# logger.error('Our First Log Message')


# machine_log = setup_logger('machine_running', 'logs/machine_running.log')
# machine_status_log = setup_logger('machine_status', 'logs/machine_status.log')
# test_log = setup_logger('test_log', 'logs/test_log.log')
