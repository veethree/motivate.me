from flask import Flask, render_template
from pexels_api import API
from random import randrange, choice
from PIL import Image, ImageFont, ImageDraw
import requests
import textwrap

PEXELS_API_KEY = "Put a valid pexels api key here"

api = API(PEXELS_API_KEY)
app = Flask(__name__)

def fetch_image():
	results = 10
	search_terms = ["landscape", "forrest", "city", "grass", "tree", "trees", "urban"]
	api.search(search_terms[randrange(len(search_terms))], page=1, results_per_page=results)
	photo = api.get_entries()
	return photo[randrange(results)]

def fetch_quote():
	lines = open("static/quote_list.txt").read().splitlines()
	return choice(lines)

def generate_image():
	url = fetch_image().landscape
	raw_quote = fetch_quote()
	img = Image.open(requests.get(url, stream=True).raw)
	width, height = img.size
	wrapped = textwrap.wrap(raw_quote, 50)
	quote = ""
	for line in wrapped:
		quote = quote + line + "\n"
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("static/BebasNeue-Regular.ttf", 50)
	draw.text((32, 32), quote, (255, 255, 255), font=font, align="left", stroke_width=2, stroke_fill=(0, 0, 0))
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