class FlaskConfigure(object):
    HOST    = '0.0.0.0'
    PORT    = 5015
    DEBUG   = True


class INITDB(object):
    """
    DÙNG KHI KHỞI TẠO DATABASE
    """
    ACTIVE = False

class Development(object):
    """
    BẬT TẮT TRANG WEB DEVELOP BACKEND
    """
    ACTIVE = True

class MqttConfigure(object):
    MQTT_BROKER_URL = '127.0.0.1'
    MQTT_BROKER_PORT    = 1883
    MQTT_USERNAME       = ''
    MQTT_PASSWORD       = ''
    MQTT_KEEPALIVE      = 5
    MQTT_TLS_ENABLED    = False
    FRONTEND_TOPIC      = '/agv/realtime'
    COM_NOTIFY_TOPIC    = '/notify_com'
    AGV_COUNT_MESSAGE   = 20
    ACTIVE              = True
    
class MysqlConfigure(object):
    HOST        = '54.169.159.150'
    # HOST        = '127.0.0.1'
    USER        = 'root'
    PASSWORD    = 'Rostek@2019'
    # PASSWORD    = '123456'

    DATABASE    = 'amr_rostek'
    # DATABASE    = 'amr'

class OperatingSystem(object):
    PASSWORD    = '1'
    BRIDGE_SERVICE = 'rostek-bridge.service'
    # ROS_BRIDGE  = 'rostek-bridge.service'
