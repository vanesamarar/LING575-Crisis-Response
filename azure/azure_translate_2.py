import os
import requests, uuid, json
from dotenv import load_dotenv

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
	#initialize translation client
	key = os.getenv("AZURE_KEY_1") #need to add key and hide .env file
	endpoint = os.getenv("AZURE_ENDPOINT") #need to add endpoint url
	region = os.getenv("AZURE_REGION")

	#dont think we need to specify location

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
		#create new file for each translated file, using category key and lang c  
		body =[{'text': content}] 
		request = requests.post(constructed_url, params=params, headers=headers, json=body)
		response=request.json()
		#print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':')))

		#parse response
		#response as a list of dictionaries
		out_path = os.path.join(lang_dir, file)
		with open(out_path, "w", encoding="utf-8") as outFile:
			outFile.write(response[0]['translations'][0]['text'])
		print(f"Translated {file} to {lang}")

def main():
	load_dotenv() #load env variables form .env file -- explain in readme
	input_dir = "data"
	output_dir = "translations"
	translation_langs = ["es", "vi", "ko", "km", "so"]
	
	alerts=load_alerts(input_dir)
	for lang in translation_langs:
		translate_text(alerts, lang, output_dir)
if __name__ == "__main__":
	main()

   #.env files create file .env hide this file and put keys in here - put in main
   # define keys key =""
   # from dotenv import load_dotenv
   #  key=os.getenv("AZURE_TRANSLATE_KEY")
   
