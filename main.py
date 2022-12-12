from sensor import Sensor
from umqtt.robust import MQTTClient
from machine import Timer
import json
import my_config as mc


# setup AWS SSL
KEY_PATH = "AWS-private.pem.key"
CERT_PATH = "AWS-certificate.pem.crt"
try:
    with open(KEY_PATH, "r") as f:
        key = f.read()
    with open(CERT_PATH, "r") as f:
        cert = f.read()
except Exception as e:
    print("Read SSL Certs", e)

# setup AWS parameters
CLIENT_ID = mc.ID
HOST = mc.AWS_HOST
PORT = 8883
SSL_PARAMS = {"key": key, "cert": cert, "server_side": False}

# setup MQTT
try:
    global client
    client = MQTTClient(client_id = CLIENT_ID,
                        server = HOST,
                        port = PORT,
                        keepalive = 10000,
                        ssl = True,
                        ssl_params = SSL_PARAMS)
    client.connect()
    print("Successfully connected to MQTT Broker.")
except Exception as e:
    print("Setup MQTT Error:", e)


def read_sensor(tmrObj):
    moist_reading = Sensor.moisture()
    j = {
            "state": {
                "reported" : {
                "moisture reading": moist_reading
                }
            }
        }

    client.publish(mc.SHADOW_UPDATE, json.dumps(j))

tmr = Timer(-1)
tmr.init(mode=Timer.PERIODIC, period=10000, callback=read_sensor)