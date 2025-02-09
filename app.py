from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():  # weather() fonksiyonu burada başlıyor
    city = request.form['city']
    api_key = os.getenv('WEATHER_API_KEY')

    if not api_key:
        return render_template('index.html', error="API key is missing.")

    API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        data = response.json()

        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
        }

        return render_template('weather.html', weather=weather_data)

    except requests.exceptions.RequestException as e:
        return render_template('index.html', error=f"Error fetching weather data: {e}")
    except (KeyError, TypeError) as e:
        return render_template('index.html', error=f"Error parsing weather data: {e}")

# weather() fonksiyonu burada bitiyor

if __name__ == '__main__':
    app.run(debug=True)