import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho

mqttc = paho.Client()
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

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

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL 0x240.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

serdev1 = '/dev/ttyACM0'
s1 = serial.Serial(serdev1, 9600)
t = np.arange(0, 20, 1)
x = np.arange(0, 20, 1)
a0 = np.arange(0, 20, 1)
a1 = np.arange(0, 20, 1)
a2 = np.arange(0, 20, 1)
time.sleep(5)
print("start sending RPC")
mqttc.publish(topic, "0.001")
for i in range(0, 20):
    # send RPC to remote
    s.write("/replyAcc/run 0 0\r".encode())
    time.sleep(0.7)
    line=s1.readline() # Read an echo string from K66F terminated with '\n'
    print(line)
    line=s1.readline() # Read an echo string from K66F terminated with '\n'
    print(line)
    x[i] = int(line)
    line=s1.readline() # Read an echo string from K66F terminated with '\n'
    print(line)
    a0[i] = float(line)
    time.sleep(0.1)
    mqttc.publish(topic, line) 
    line=s1.readline() # Read an echo string from K66F terminated with '\n'
    print(line)
    a1[i] = float(line)
    time.sleep(0.1)
    mqttc.publish(topic, line) 
    line=s1.readline() # Read an echo string from K66F terminated with '\n'
    print(line)
    a2[i] = float(line)
    time.sleep(0.1)
    mqttc.publish(topic, line) 


fig, ax = plt.subplots(1, 1)
ax.plot(t,x)
ax.set_xlabel('number')
ax.set_ylabel('timestamp')
plt.show()
s.close()