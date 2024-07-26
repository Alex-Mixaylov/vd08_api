from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        weather, error = get_weather(city)
    return render_template("index.html", weather=weather, error=error)

def get_weather(city):
    api_key = "d910ee490c508d67d15d77ec547f829d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, "Город не найден или произошла ошибка."

if __name__ == '__main__':
    app.run(debug=True)
