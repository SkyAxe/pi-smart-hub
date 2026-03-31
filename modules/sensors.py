import adafruit_dht
import board

class IndoorSensor:
    def __init__(self):
        # We connected the "S" pin to GPIO 4 (Pin 7)
        self.sensor = adafruit_dht.DHT11(board.D4)

    def get_reading(self):
        try:
            temperature_c = self.sensor.temperature
            humidity = self.sensor.humidity
            
            if humidity is not None and temperature_c is not None:
                return {
                    "temp": f"{temperature_c:.1f}",
                    "hum": f"{humidity}"
                }
        except RuntimeError as error:
            # DHT sensors are finicky; errors happen often, just retry
            print(f"Sensor read error: {error.args[0]}")
            return None
        except Exception as e:
            self.sensor.exit()
            raise e
        return None
