from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            error = "Lütfen bir şehir adı girin."
        else:
            return redirect(url_for('forecast_page', city=city))
    return render_template('index.html', error=error)

@app.route('/forecast_page')
def forecast_page():
    city = request.args.get('city')
    if not city:
        return redirect(url_for('index', error="Please provide a city name."))

    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return render_template('index.html', error="API anahtarı eksik.")

    API_URL = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        daily_temps = {}
        for entry in data['list']:
            date = entry['dt_txt'].split()[0]
            temp = entry['main']['temp']

            if date not in daily_temps:
                daily_temps[date] = []
            daily_temps[date].append(temp)

        avg_temps = {date: sum(temps) / len(temps) for date, temps in daily_temps.items()}

        # Grafik oluşturma ve kaydetme
        plt.figure(figsize=(10, 5))
        plt.plot(avg_temps.keys(), avg_temps.values(), marker='o', linestyle='-', color='b')
        plt.xlabel('Tarih', fontsize=12)
        plt.ylabel('Sıcaklık (°C)', fontsize=12)
        plt.title(f"{city} için 5 Günlük Hava Durumu Tahmini", fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Dosyaya kaydetmek yerine base64 string olarak döndür
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return render_template('forecast_page.html', city=city, plot_url=plot_url)

    except requests.exceptions.RequestException as e:
        return render_template('index.html', error=f"Hava durumu verisi alınırken hata oluştu: {e}")
    except (KeyError, TypeError) as e:
        return render_template('index.html', error=f"Hava durumu verileri ayrıştırılırken hata oluştu. Yanıt yapısı değişmiş olabilir. Detaylar: {e}")

if __name__ == '__main__':
    app.run(debug=True)


