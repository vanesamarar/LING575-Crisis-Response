import os
from dotenv import load_dotenv
import requests, uuid, json

def load_alerts(input_dir):
	alerts = []
	for root, _, files in os.walk(input_dir):
		for file in sorted(files):
			if file.endswith(".txt"):
				full_path = os.path.join(root, file)
				with open(full_path, "r", encoding="utf-8") as f:
					content = f.read()
				alerts.append((file, content))
	return alerts

def translate_text(alerts, lang):
	key=os.getenv("AZURE_KEY_2") #need to add key and hide .env file
	endpoint=os.getenv("AZURE_ENDPOINT") #need to add endpoint url to .env ---- I THINK this can be the same endpoint url as forward translation
	region = os.getenv("AZURE_REGION", "westus2")

	path='/translate'
	constructed_url=endpoint +path
	params={
		'api-version':'3.0',
		'from':lang,
		'to':'en'
	}
	headers={
		'Content-type':'application/json',
		'X-ClientTraceId':str(uuid.uuid4()),
		'Ocp-Apim-Subscription-Key':key,
		'Ocp-Apim-Subscription-Region': region 
	}

	output_dir = os.path.join("azure", "back_translations", lang)
	os.makedirs(output_dir, exist_ok=True)

	for fname, content in alerts:
		body = [{'text': content}]
		response = requests.post(constructed_url, params=params, headers=headers, json=body)
		response_json = response.json()

		backtrans = response_json[0]['translations'][0]['text']
		out_path = os.path.join(output_dir, fname)
		with open(out_path, "w", encoding="utf-8") as out_f:
			out_f.write(backtrans)

def main():
	load_dotenv()
	langs = ["es", "vi", "ko", "km", "so"]

	for lang in langs:
		input_dir = os.path.join("azure", "forward_translations", lang)
		alerts = load_alerts(input_dir)
		translate_text(alerts, lang)
	

if __name__ == "__main__":
	main()
   
