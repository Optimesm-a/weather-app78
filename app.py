from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '31f68c4043b01c7129698874d321e9c6'  # Burada, hava durumu API anahtarınızı kullanmalısınız
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


    app.run(debug=True)
