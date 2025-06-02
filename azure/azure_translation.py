import os
import requests, uuid, json
from dotenv import load_dotenv

translation_langs = ["es", "vi", "ko", "km", "so"]
input_dir = "data"
output_dir = "azure/forward_translations"

def load_alerts(data_dir):
	alerts = []
	for root, _, files in os.walk(data_dir):
		for file in files:
			if file.endswith(".txt"):
				full_path = os.path.join(root, file)
				with open(full_path, "r", encoding="utf-8") as f:
					content = f.read()
				alerts.append((file, content))
	return alerts

def translate_text(alerts, lang, out_dir):
	key = os.getenv("AZURE_KEY_1") 
	endpoint = os.getenv("AZURE_ENDPOINT") 
	region = os.getenv("AZURE_REGION")
	assert key and endpoint and region, "Missing Azure environment variables."

	path = '/translate'
	constructed_url = endpoint + path
	params = {
		'api-version':'3.0',
		'from':'en',
		'to':lang
	}
	headers = {
		'Content-type':'application/json',
		'X-ClientTraceId':str(uuid.uuid4()),
		'Ocp-Apim-Subscription-Key':key,
		'Ocp-Apim-Subscription-Region': region #need to check this, otherwise optional
	}

	lang_dir = os.path.join(out_dir, lang)
	os.makedirs(lang_dir, exist_ok=True)

	for file, content in alerts:
		body =[{'text': content}] 
		request = requests.post(constructed_url, params=params, headers=headers, json=body)
		response=request.json()
		if "error" in response:
			print(f"Error translating {file} to {lang}: {response['error']}")
			continue
		translated_text = response[0]['translations'][0]['text']

		out_path = os.path.join(lang_dir, file)
		with open(out_path, "w", encoding="utf-8") as outFile:
			outFile.write(translated_text)
		print(f"Translated {file} to {lang}")

def main():
	load_dotenv()

	print("AZURE_KEY_1:", os.getenv("AZURE_KEY_1"))
	print("AZURE_ENDPOINT:", os.getenv("AZURE_ENDPOINT"))
	print("AZURE_REGION:", os.getenv("AZURE_REGION"))
 
	alerts=load_alerts(input_dir)
	for lang in translation_langs:
		translate_text(alerts, lang, output_dir)
if __name__ == "__main__":
	main()
   
