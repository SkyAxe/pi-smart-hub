from flask import Flask, render_template, Response
import os, json
from dotenv import load_dotenv
from modules.weather import WeatherModule
from modules.calendar import CalendarModule
from modules.sensors import IndoorSensor

load_dotenv()

app = Flask(__name__)
weather        = WeatherModule(city="Leipzig", api_key=os.getenv("OPENWEATHER_API_KEY"))
calendar_mod   = CalendarModule()
indoor         = IndoorSensor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    weather_data = weather.get_data()
    indoor_data  = indoor.get_reading() or {"temp": "--", "hum": "--"}
    try:
        events = calendar_mod.get_upcoming_events()
    except Exception as e:
        print(f"Calendar error: {e}")
        events = {}

    data = {
        "temp":        weather_data.get("temp",       "--"),
        "feels_like":  weather_data.get("feels_like", "--"),
        "humidity":    weather_data.get("humidity",   "--"),
        "wind":        weather_data.get("wind",       "--"),
        "desc":        weather_data.get("desc",       "--"),
        "icon":        weather_data.get("icon",       "01d"),
        "indoor_temp": indoor_data.get("temp",        "--"),
        "indoor_hum":  indoor_data.get("hum",         "--"),
        "events":      events,
    }
    return Response(
        json.dumps(data, ensure_ascii=False, sort_keys=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
