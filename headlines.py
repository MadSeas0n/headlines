from flask import render_template
import feedparser
from flask import Flask
from flask import request

app = Flask(__name__)

RSS_FEEDS = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
            "lenta": "https://lenta.ru/rss/top7",
            "rambler_msk": "https://news.rambler.ru/rss/moscow_city/",
            "ya_scn": "https://news.yandex.ru/science.rss"
            }


@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed["entries"])


if __name__ == '__main__':
    app.run(port=5000, debug=True)

