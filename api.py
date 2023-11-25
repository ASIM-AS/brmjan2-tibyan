import requests
from PIL import Image
import io
import base64

# FILTER

import re
def clean_string(input_string):
    # Lowercase the string and remove non-alphabetic characters
    cleaned_string = re.sub(r'[^a-z]', '', input_string.lower())
    return cleaned_string
with open("invalid_searches.txt", 'r') as f:
	invalid = f.readlines()
	invalid = [clean_string(i) for i in invalid]
	invalid = [i for i in invalid if i != ""]
	invalid.append("")
def check_invalid(word):
	word = clean_string(word)
	return word in invalid

# GETTING THE KEYS

# from keys import *
import os
HF_TOKEN = os.environ.get('HF_TOKEN')
DICTIONARY_API_KEY = os.environ.get('DICTIONARY_API_KEY')

def get_definition(word):

	url = 'https://siwar.ksaa.gov.sa/api/alriyadh/exact-search'
	headers = {
		'accept': 'application/json',
		'apikey': DICTIONARY_API_KEY
	}
	params = {'query': word}
	response = requests.get(url, params=params, headers=headers)
	print(response)

	# word not found
	define = response.json()
	if len(define) == 0:
		return "", "",  []

	define = define[0]

	word = define['lemma']['formRepresentations'][0]['form']
	english = None
	meanings_examples = []

	for i, sense in enumerate(define['senses']):
		meaning = sense['definition']['textRepresentations'][0]['form']
		example = None
		for ex in sense['examples']:
			if ex['form'] != "":
				example = ex['form']
		for ex in sense['translations']:
			if ex['form'] != "" and not english:
				english = ex['form']

		meanings_examples.append({
			"i": i+1,
			"meaning": meaning,
			"example": example
		})

	return word, english, meanings_examples

def get_translation(word):

	if word == "":
		return ""

	API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-ar-en"
	headers = {"Authorization": f"Bearer {HF_TOKEN}"}

	response = requests.post(API_URL, headers=headers, json={
		"inputs": word,
	})
	print(response)
	response = response.json()
	print(response)

	# error in response
	if type(response) == dict:
		return ""

	return response[0]['translation_text']

def get_image(word):

	print(word)

	if check_invalid(word):
		return None
		# blank image
		return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

	API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
	headers = {"Authorization": f"Bearer {HF_TOKEN}"}

	response = requests.post(API_URL, headers=headers, json={
		"inputs": word,
	})
	print(response)
	image_bytes = response.content

	image = Image.open(io.BytesIO(image_bytes))

	# Convert image to base64
	image_base64 = ""
	with io.BytesIO() as buffer:
		image.save(buffer, format="JPEG")
		image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
	
	return image_base64


if __name__ == "__main__":
	pass




