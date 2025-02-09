from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = os.getenv('WEATHER_API_KEY')  # API anahtarını .env dosyasından al

    if not api_key:
        return render_template('index.html', error="API key is missing.")

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data.get('cod') != 200:
        return render_template('index.html', error="City not found.")

    weather_data = {
        'city': city,
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
    }

    return render_template('weather.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)



