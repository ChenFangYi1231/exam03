import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "velocity"
x = np.arange(0, 2, 0.1)
y = np.arange(0, 2, 0.1)
t = np.arange(0, 2, 0.1)
temp = np.arange(0, 2, 0.1)

# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");
      temp[0] = float(msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

done = 1
while done:
      mqttc.loop()
      if temp[0] == 0.001:
            done = 0
      print("waiting...")
      time.sleep(1)
print("start")
for i in range(0,20):
      time.sleep(0.05)
      mqttc.loop()
      x[i] = temp[0]
      print(x[i])
      time.sleep(0.05)
      mqttc.loop()
      y[i] = temp[0]
      print(y[i])
      
fig, ax = plt.subplots(1, 1)
ax.plot(t,x, 'b', label = 'x', color = 'b')
ax.plot(t,y, 'r', label = 'y', color = 'r')
ax.set_xlabel('Time')
ax.set_ylabel('velocity')
ax.legend()
plt.show()
      
