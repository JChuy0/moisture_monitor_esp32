"""A MQTT Client"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import json
import ssl
import time
import my_config as mc

moist_list = []
time_list = []

def on_connect(client, userdata, flags, rc):
    """Event happens on connection to broker."""

    try:
        print(f"Successfully connected with result code: {rc}")
        client.subscribe(mc.SHADOW_GET_ACCEPTED)
        client.subscribe(mc.SHADOW_GET_REJECTED)
        client.subscribe(mc.SHADOW_UPDATE_ACCEPTED)
        client.subscribe(mc.SHADOW_UPDATE_REJECTED)
    except Exception as e:
        print(e)

def on_message(client, userdata, msg):
    """Event happens when recieved message from broker."""

    try:
        d = json.loads(msg.payload)
        data = d["state"]["reported"]["moisture reading"]

        global moist_list
        global time_list

        moist_list.append(data["percent"])
        time_list.append(data["timestamp"])

        if len(moist_list) > 60:
            del moist_list[:1]
        
        if len(time_list) > 60:
            del time_list[:1]

        print(data)

    except Exception as e:
        print(e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# setup SSL/TLS
client.tls_set(ca_certs = "AmazonRootCA1.pem",
                certfile = "AWS-certificate.pem.crt",
                keyfile = "AWS-private.pem.key",
                cert_reqs = ssl.CERT_REQUIRED,
                tls_version = ssl.PROTOCOL_TLS,
                ciphers = None)

# connect to AWS MQTT server
client.connect(mc.AWS_HOST, 8883, 60)
client.loop_start()


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global moist_list
    global time_list

    ax1.clear()
    ax1.plot(time_list, moist_list)
    ax1.set_title("Soil Moisture", loc="center", y = 1, x = 0.5)
    ax1.set_ylabel("Percent")
    ax1.grid()

    # rotates and aligns the x labels 
    for label in ax1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')

ani = animation.FuncAnimation(fig, animate, interval=10000)
plt.show()

while True:
    client.publish(mc.SHADOW_GET, json.dumps({}))

    time.sleep(10)
