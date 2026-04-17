from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from environment variable (recommended practice)
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'YOUR_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required!'}), 400
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'City not found!'})
    data = response.json()
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed']
    }
    return jsonify(weather)

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes', 'on')
    app.run(debug=debug_mode)
