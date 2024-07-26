from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    quote = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        weather, error = get_weather(city)
        if not error:
            quote, error = get_random_quote()
        if not error:
            news, error = get_news()
    return render_template("index.html", weather=weather, news=news, quote=quote, error=error)

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
        # Ограничиваем количество новостей до 7
        articles = response.json().get('articles', [])
        return articles[:7], None
    else:
        return None, "Произошла ошибка при получении новостей."

def get_random_quote():
    api_key = "f115209b4cmsh517b193399e84d0p164af3jsndbe9e171d02b"
    url = "https://quotes15.p.rapidapi.com/quotes/random/"
    querystring = {"language_code": "ru"}

    headers = {
        'x-rapidapi-host': "quotes15.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        quote_data = response.json()
        return {
            "content": quote_data.get('content', 'No content available'),
            "name": quote_data.get('originator', {}).get('name', 'Unknown')
        }, None
    else:
        return None, "Произошла ошибка при получении цитаты."

if __name__ == '__main__':
    app.run(debug=True)
