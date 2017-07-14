from flask import render_template
import feedparser
from flask import Flask
from flask import request
from urllib.request import urlopen
from urllib.parse import quote
import json
import datetime
from flask import make_response

app = Flask(__name__)

RSS_FEEDS = {
            "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
            "lenta": "https://lenta.ru/rss/top7",
            "rambler_msk": "https://news.rambler.ru/rss/moscow_city/",
            "ya_scn": "https://news.yandex.ru/science.rss"
            }

DEFAULTS = {
            "publication": "bbc",
            "city": "Moscow,RU",
            "currency_from": "EUR",
            "currency_to": "RUB"
            }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=6026d8c90a4244dfc0548344ab24cf7a"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=a0357e1c461548738e249ccfddc5302e"


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)


@app.route("/")
def home():
    # RSS
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # Weather
    city = get_value_with_fallback("city")
    weather = get_weather(city)
    # Currency
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    # Save cookies abd return template
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now()+datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed["entries"]


def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"]
        }
    return weather


def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate, parsed.keys()


if __name__ == '__main__':
    app.run(port=5000, debug=True)

