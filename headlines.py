from flask import render_template
import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEED = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
            "lenta": "https://lenta.ru/rss/top7",
            "rambler_msk": "https://news.rambler.ru/rss/moscow_city/",
            "ya_scn": "https://news.yandex.ru/science.rss"
            }


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEED[publication])
    return render_template("home.html", articles=feed["entries"])


if __name__ == '__main__':
    app.run(port=5000, debug=True)

