from flask import Flask, request, render_template

from api import (
	get_definition,
	get_translation,
	get_image,
)
# from test_api import (
	# get_definition,
	# get_translation,
	# get_image,
# )

app = Flask(__name__)

@app.route('/')
def index():
	word = request.args.get('word', None)

	# HOME PAGE NO WORD YET
	if word == None:
		return render_template("index.html", data=None)

	# 1. GET DEFINITION
	print("-------> get_definition")
	word, english, meanings_examples = get_definition(word)

	# 2. GET TRANSLATION
	print("-------> get_translation")
	if not english:
		english = get_translation(word)

	# 3. GET IMAGE
	print("-------> get_image")
	img = get_image(english)

	print("-------> return_data")
	# 4. RETURN DATA
	data = {
		"word": word,	# 1, 2
		"english": english,	# 5
		"img": img,	# 6
		"meanings_examples": meanings_examples,	# 3, 4
	}
	return render_template("index.html", data=data)

if __name__ == '__main__':
	app.run(debug=True)
	# app.run()
