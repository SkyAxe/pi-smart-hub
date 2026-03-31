from flask import Flask, render_template, jsonify
import datetime
from modules.weather import WeatherModule
from modules.calendar import CalendarModule
from modules.sensors import IndoorSensor

app = Flask(__name__)

# Initialize your modules here
weather = WeatherModule(city="Leipzig", api_key="af4124db2382f2fc9b0c49b3435ac240")
calendar = CalendarModule()
indoor = IndoorSensor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    weather_data = weather.get_data()
    events = calendar.get_upcoming_events()
    indoor_data = indoor.get_reading() or {"temp": "--", "hum": "--"}

    return jsonify({
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
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
