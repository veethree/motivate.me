from flask import Flask, render_template
from pexels_api import API
from random import randrange, choice
from PIL import Image, ImageFont, ImageDraw
import requests
import textwrap
import json

PEXELS_API_KEY = "Insert your pexels api key here"

api = API(PEXELS_API_KEY)
app = Flask(__name__)

with open("static/quotes.json", "r") as file:
	quote_list = json.load(file)

def fetch_image():
	results = 10
	search_terms = ["landscape", "forrest", "city", "grass", "tree", "trees", "urban"]
	api.search(search_terms[randrange(len(search_terms))], page=1, results_per_page=results)
	photo = api.get_entries()
	return photo[randrange(results)]

def fetch_quote():
	quote = choice(quote_list)
	return quote

def generate_image():
	url = fetch_image().landscape
	raw_quote = fetch_quote()
	img = Image.open(requests.get(url, stream=True).raw)
	quote = raw_quote["quote"].strip('"')
	author = raw_quote["author"]
	wrapped = textwrap.wrap(quote, 40)
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("static/BebasNeue-Regular.ttf", 50)
	y = 32
	for line in wrapped:
		draw.text((32, y), line, (255, 255, 255), font=font, align="center", stroke_width=2, stroke_fill=(0, 0, 0))
		y += 40

	draw.text((900, 500), author, (255, 255, 255), font=font, align="right", stroke_width=2, stroke_fill=(0, 0, 0))
	img.save("static/temp.jpg")


@app.route("/")
def index():
	generate_image()
	return render_template("index.html", img=fetch_image())

@app.route("/about")
def about():
	return render_template("about.html")


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")