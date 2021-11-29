import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class MqttSingle:
	__hostname= '127.0.0.1'
	__port = 1883

	@staticmethod
	def publish(topic, payload):
		return publish.single( topic=topic, payload=payload, hostname=MqttSingle.__hostname, port=MqttSingle.__port, protocol=mqtt.MQTTv311)
