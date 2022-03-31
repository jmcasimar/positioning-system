#!/usr/bin/env python3
import os
import sys
import json
from time import time, sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
sys.path.insert(0, './src/')
from logger import logger
from configManager import configManager
from mqttCallback import mqttController
from bluetoothManager import devicesManager

# Check if temp dir exists, if not then create it
if not os.path.exists('temp/'): os.makedirs('temp/')

# Initialize configManager
config = configManager()

# Define logger
log = logger()

# Define the Manager
manager = devicesManager(config, log)

# Define mqtt callbacks
mqttControl = mqttController(manager, log)

# Aux variables
positionTimer = time()

try:
    # Define MQTT communication
    client = mqtt.Client()
    client.on_connect = mqttControl.on_connect  # Specify on_connect callback
    client.on_message = mqttControl.on_message  # Specify on_message callback
    #client.on_publish = mqttController.on_publish  # Specify on_publish callback
    client.on_disconnect = mqttControl.on_disconnect  # Specify on_disconnect callback
    # Connect to MQTT broker. Paremeters (IP direction, Port, Seconds Alive)
    if(client.connect(config.brokerIP, 1883, 60)==0): mqttControl.clientConnected = True
    else: log.logger.error("Cannot connect with MQTT Broker")
except Exception as e: log.logger.error("Cannot connect with MQTT Broker [{}]".format(e))

while True:
    # Update positions once per minute
    if(time()-positionTimer>=60):
        positionTimer = time()
        manager.getBeaconsPositions()

     # If mqtt connected check for messages
    if mqttControl.clientConnected: client.loop(0.1)
    else:
        sleep(0.1)
        # Else try to reconnect every 30s
        if(time()-mqttControl.actualTime>30):
            mqttControl.actualTime = time()
            try:
                # Reconnect client
                client = mqtt.Client()
                client.on_connect = mqttControl.on_connect  # Specify on_connect callback
                client.on_message = mqttControl.on_message  # Specify on_message callback
                #client.on_publish = mqttController.on_publish  # Specify on_publish callback
                client.on_disconnect = mqttControl.on_disconnect  # Specify on_disconnect callback
                # Connect to MQTT broker. Paremeters (IP direction, Port, Seconds Alive)
                if(client.connect(config.brokerIP, 1883, 60)==0): mqttControl.clientConnected = True
                else: log.logger.error("Cannot connect with MQTT Broker")

            except Exception as e: log.logger.error("Cannot connect with MQTT Broker [{}]".format(e))