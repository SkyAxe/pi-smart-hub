# -*- coding: utf-8 -*-
import requests
import time

class WeatherModule:
    def __init__(self, city, api_key):
        self.city = city
        self.api_key = api_key
        self.cache = {
            "temp": "--", 
            "feels_like": "--",
            "desc": "Loading...", 
            "humidity": "--",
            "wind": "--",
            "icon": "01d" # Default sun icon
        }
        self.last_update = 0

    def get_data(self):
        now = time.time()
        if now - self.last_update > 900:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    self.cache["temp"] = f"{round(data['main']['temp'])}\u00b0C"
                    self.cache["feels_like"] = f"{round(data['main']['feels_like'])}\u00b0C"
                    self.cache["desc"] = data['weather'][0]['description'].capitalize()
                    self.cache["humidity"] = f"{data['main']['humidity']}%"
                    self.cache["wind"] = f"{data['wind']['speed']} m/s"
                    self.cache["icon"] = data['weather'][0]['icon']
                    self.last_update = now
            except Exception as e:
                print(f"Weather Module Error: {e}")
        return self.cache
