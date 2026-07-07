# -*- coding: utf-8 -*-
import threading

try:
    import board, adafruit_dht
    _PI = True
except (ImportError, NotImplementedError):
    _PI = False

class IndoorSensor:
    def __init__(self):
        if not _PI:
            print("Sensor: kein Pi erkannt – nutze Mockdaten")
            self._ok = False
            return
        try:
            self.sensor = adafruit_dht.DHT11(board.D4)
            self._ok = True
        except Exception as e:
            print(f"Sensor init failed: {e}")
            self._ok = False

    def get_reading(self):
        if not _PI:
            return {"temp": 22.5, "hum": 55}  # Mock für lokale Entwicklung
        if not self._ok:
            return {"temp": None, "hum": None}
        result = {}
        def read():
            try:
                t, h = self.sensor.temperature, self.sensor.humidity
                if t is not None and h is not None:
                    result["temp"] = round(t, 1)
                    result["hum"]  = round(h)
            except Exception as e:
                print(f"Sensor error: {e}")
        thread = threading.Thread(target=read, daemon=True)
        thread.start()
        thread.join(timeout=3.0)
        return {"temp": result.get("temp"), "hum": result.get("hum")}
