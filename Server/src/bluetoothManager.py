#!/usr/bin/env python3
import json
import datetime
from triangulation import triangulation

class Client:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def returnPosition(self): return [self.x, self.y, self.z]

class bluetoothDevice:
    def __init__(self, data = {"mac": "00:00:00:00:00:00"}, clientData = {}):
        self.data = data
        self.mac = data["mac"]
        self.distance = {}
        for client in clientData: self.distance[client] = 0
    
    def updateDistance(self, client, dist):
        self.distance[client] = dist

    def getDistances(self, clientData):
        distances = []
        for client in clientData: distances.append(self.distance[client])
        return distances

class devicesManager:
    def __init__(self, config, logger):
        # Save configuration for later use
        self.config = config
        # Save the logger
        self.log = logger

        # Initialize devices and positions
        self.devices = {}
        self.positions = {}
        for device in config.bluetoothMac: 
            self.devices[device] = bluetoothDevice(config.bluetoothMac[device], config.clients)
            self.positions[device] = [0, 0, 0]

        # Define Clients
        self.clients = {}
        for client in config.clients: 
            self.clients[client] = Client(float(config.clients[client]["x"]), 
                                          float(config.clients[client]["y"]),  
                                          float(config.clients[client]["z"]))

    def returnClientPositions(self, clients):
        positions = []
        for client in clients: positions.append(self.clients[client].returnPosition())
        return positions

    def getBeaconsPositions(self):
        pos = self.returnClientPositions(self.config.clients)
        for device in self.devices:
            dist = self.devices[device].getDistances(self.config.clients)
            self.positions[device] = triangulation(pos, dist)
            mssg = {"timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"id":device,"position":{"x":str(self.positions[device][0]),  "y":str(self.positions[device][1]), "z":str(self.positions[device][2])} }
            self.log.logger_positions.info(json.dumps(mssg))
        self.log.logger.info("")

    