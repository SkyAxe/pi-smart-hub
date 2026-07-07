# -*- coding: utf-8 -*-
import requests
import time

class WeatherModule:
    def __init__(self, city, api_key):
        self.city = city
        self.api_key = api_key
        self.cache = {
            "temp":       None,
            "feels_like": None,
            "desc":       "L\u00e4dt...",
            "humidity":   None,
            "wind":       None,
            "icon":       "01d",
        }
        self.last_update = 0

    def get_data(self):
        now = time.time()
        if now - self.last_update > 900:
            try:
                url = (
                    f"http://api.openweathermap.org/data/2.5/weather"
                    f"?q={self.city}&appid={self.api_key}&units=metric&lang=de"
                )
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    self.cache["temp"]       = round(data["main"]["temp"])
                    self.cache["feels_like"] = round(data["main"]["feels_like"])
                    self.cache["desc"]       = data["weather"][0]["description"].capitalize()
                    self.cache["humidity"]   = data["main"]["humidity"]
                    self.cache["wind"]       = round(data["wind"]["speed"], 1)
                    self.cache["icon"]       = data["weather"][0]["icon"]
                    self.last_update = now
            except Exception as e:
                print(f"Weather error: {e}")
        return self.cache
