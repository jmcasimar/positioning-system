#!/usr/bin/env python3

import json

class configManager:
    def __init__(self):
        # Charge data
        self.load()
    
    def load(self):
        # Load data
        with open("config.json", "r") as f:
            self.data = json.load(f)
        # Extract important variables
        self.bluetoothMac = self.data["bluetoothDevices"]
        self.clients = self.data["clients"]
        self.brokerIP = self.data["brokerIP"]

    def saveConfig(self):
        # Save data
        with open("config.json", "w") as f:
            self.data["bluetoothDevices"] = self.bluetoothMac
            self.data["clients"] = self.clients
            self.data["brokerIP"] = self.brokerIP
            json.dump(self.data, f, indent=4)
    
    def addBeacon(self, name, data):
        # Data at least need "mac", "rssi_always"[bool] and "rx_power"
        self.bluetoothMac[name] = data
        self.saveConfig()

    def addClient(self, name, data):
        # Data at least need "x", "y" and "z"
        self.clients[name] = data
        self.saveConfig()