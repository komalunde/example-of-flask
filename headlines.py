import json
import urllib2
import urllib
import feedparser
from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

RSS_FEEDS={'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
	'cnn':'http://rss.ccn.com/rss/edition.rss',
	'fox':'http: //feeds.foxnews.com/foxnews /latest',
	'iol':'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route("/bbc")
def bbc():
	return get_news('bbc')

@app.route("/cnn")
def cnn():
	return get_news('cnn')

DEFACULTS={'publication':'bbc',
		   'city':'London,UK'}

@app.route("/")
def home():
	publication=request.args.get('publication')
	if not publication:
		publication=DEFACULTS['publication']
		articles=get_news(publication)
		city=request.args.get('city')
		if not city:
			city=DEFACULTS['city']
			weather=get_weather(city)
		return render_template("home.html",
				articles=articles,weather=weather)


@app.route("/<publication>")
def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication=DEFACULTS["publication"]
	else:
		publication=query.lower()
		feed=feedparser.parse(RSS_FEEDS[publication])
		return feed['entries']

def get_news(publication):
	query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
			publication="bbc"
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	weather = get_weather("london")
	return render_template("home.html", articles=feed["entries"], weather=weather)


def get_weather(query):
	api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cb3823bdd1813a699aa834b14a69cb99'

	query = urllib.quote(query)
	url = api_url.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather=None
	if parsed.get("weather"):
		weather={"description":
				 parsed["weather"][0]["description"],
				 "temperature":parsed["main"]["temp"],
				 "city":parsed["name"]
				 }
		return weather


if __name__=='__main__':
   	app.run(port=5000,debug=True)
