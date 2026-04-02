from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import datetime
import os
import json
import threading
from flask import Response
from dotenv import load_dotenv
from modules.weather import WeatherModule
from modules.calendar import CalendarModule
from modules.sensors import IndoorSensor
from modules.voice import VoiceModule
from modules.claude_ai import ask_claude

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smarthub'
socketio = SocketIO(app, cors_allowed_origins="*")

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

def on_voice_trigger(command):
    """Called when trigger word detected"""
    socketio.emit('claude_thinking', {'status': 'thinking'})
    
    try:
        # Get current context
        weather_data = weather.get_data()
        indoor_data = indoor.get_reading() or {"temp": "--", "hum": "--"}
        context = f"Aktuelle Wetterdaten: {weather_data}. Innenklima: {indoor_data}."
        
        if not command:
            command = "Hallo, was kann ich für dich tun?"

        result = ask_claude(command, context)
        
        socketio.emit('claude_response', {
            'text': result['text'],
            'model': result['model'],
            'command': command
        })
    except Exception as e:
        socketio.emit('claude_response', {
            'text': f'Fehler: {str(e)}',
            'model': 'error',
            'command': command
        })
    finally:
        voice.set_processing_done()

def on_listening():
    socketio.emit('claude_listening', {})

voice = VoiceModule(
    on_trigger_callback=on_voice_trigger,
    on_listening_callback=on_listening
)

if __name__ == '__main__':
    voice = VoiceModule(on_trigger_callback=on_voice_trigger)
    voice.start()
    socketio.run(app, host='0.0.0.0', port=5000)