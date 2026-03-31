from flask import Flask, render_template, jsonify
import datetime
import os
import json
from flask import Response
from dotenv import load_dotenv
from modules.weather import WeatherModule
from modules.calendar import CalendarModule
from modules.sensors import IndoorSensor

load_dotenv()

app = Flask(__name__)

weather = WeatherModule(city="Leipzig", api_key=os.getenv("OPENWEATHER_API_KEY"))
calendar = CalendarModule()
indoor = IndoorSensor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    weather_data = weather.get_data()
    indoor_data = indoor.get_reading() or {"temp": "--", "hum": "--"}

    try:
        events = calendar.get_upcoming_events()
    except Exception as e:
        print(f"Calendar error: {e}")
        events = {}

    data = {
        "time": datetime.datetime.now().strftime("%H:%M"),
        "date": datetime.datetime.now().strftime("%A, %b %d"),
        "temp": weather_data["temp"],
        "indoor_temp": indoor_data["temp"],
        "indoor_hum": indoor_data["hum"],
        "feels_like": weather_data["feels_like"],
        "humidity": weather_data["humidity"],
        "icon": weather_data["icon"],
        "news": weather_data["desc"],
        "events": events
    }

    # sort_keys=False verhindert alphabetische Sortierung
    return Response(
        json.dumps(data, ensure_ascii=False, sort_keys=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)