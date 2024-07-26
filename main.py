from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        weather, error = get_weather(city)
        news, error = get_news()
    return render_template("index.html", weather=weather, news=news, error=error)

def get_weather(city):
    api_key = "d910ee490c508d67d15d77ec547f829d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, "Город не найден или произошла ошибка."

def get_news():
    api_key = "02d610c099184e36a958fdf51270787e"
    url = f"https://newsapi.org/v2/everything?q=travel&language=ru&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', []), None
    else:
        return None, "Произошла ошибка при получении новостей."

if __name__ == '__main__':
    app.run(debug=True)
