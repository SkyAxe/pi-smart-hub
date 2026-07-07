# -*- coding: utf-8 -*-
import board
import adafruit_dht

class IndoorSensor:
    def __init__(self):
        try:
            self.sensor = adafruit_dht.DHT11(board.D4)
            self._available = True
        except Exception as e:
            print(f"Sensor init failed: {e}")
            self._available = False

    def get_reading(self):
        if not self._available:
            return {"temp": None, "hum": None}
        try:
            temp = self.sensor.temperature
            hum  = self.sensor.humidity
            if temp is not None and hum is not None:
                return {"temp": round(temp, 1), "hum": round(hum)}
            return {"temp": None, "hum": None}
        except Exception as e:
            print(f"Sensor read error: {e}")
            return {"temp": None, "hum": None}
