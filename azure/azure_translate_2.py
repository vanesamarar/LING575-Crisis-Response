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
	key=os.getenv("AZURE_KEY_1") #need to add key and hide .env file
	endpoint=os.getenv("AZURE_ENDPOINT") #need to add endpoint url

	#dont think we need to specify location

	path='/translate'
	constructed_url=endpoint +path
	params={
		'api-version':'3.0',
		'from':'en',
		'to':lang
	}
	headers={
		'Content-type':'application/json',
		'X-ClientTraceId':str(uuid.uuid4()),
		'Ocp-Apim-Subscription-Key':key,
		'Ocp-Apim-Subscription-Region':'westus2' #need to check this, otherwise optional
	}

	for k, value in alerts.items():
		#create new file for each translated file, using category key and lang c 
		with open(f"{k}_{lang}.txt", "w") as outFile: 
			body =[{'text': value}]
			#make request to azure translation service   
			request = requests.post(constructed_url, params=params, headers=headers, json=body)
			response=request.json()
			#print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':')))

			#parse response
			#response as a list of dictionaries
			outFile.write(response[0]['translations'][0]['text'])
		outFile.close()

def main():
	load_dotenv() #load env variables form .env file -- explain in readme
	
	alerts=load_alerts("data")
	
	#translate to target languages:
	translate_text(alerts, "es")	#Spanish translation
	translate_text(alerts, "vi")	#Vietnamese translation
	translate_text(alerts, "ko")	#Korean translation	
	translate_text(alerts, "km")	#Khmer translation
	translate_text(alerts, "so")	#Somali translation
if __name__ == "__main__":
	main()

   #.env files create file .env hide this file and put keys in here - put in main
   # define keys key =""
   # from dotenv import load_dotenv
   #  key=os.getenv("AZURE_TRANSLATE_KEY")
   
