import os
from dotenv import load_dotenv
import requests, uuid, json


#add key and endpoint -- put key and endpoint in .env file
#key = my api key is listed in my azure portal
 #not sure this is correct..... azure doesnt list my endpoints
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
	#initialize translation client - utilizes second azure API key
	key=os.getenv("AZURE_KEY_2") #need to add key and hide .env file
	endpoint=os.getenv("AZURE_ENDPOINT") #need to add endpoint url to .env ---- I THINK this can be the same endpoint url as forward translation


	path='/translate'
	constructed_url=endpoint +path
	params={
		'api-version':'3.0',
		'from':lang,
		'to':"en"
	}
	headers={
		'Content-type':'application/json',
		'X-ClientTraceId':str(uuid.uuid4()),
		'Ocp-Apim-Subscription-Key':key,
		'Ocp-Apim-Subscription-Region':'westus2' #need to check this, otherwise optional
	}

	output_dir = os.path.join("azure", "back_translations", lang)
    	os.makedirs(output_dir, exist_ok=True)

	'''for k, value in alerts.items():
		#create new file for each translated file, using category key and lang c 
		with open(f"{k}_{lang}_en_.txt", "w") as outFile: 
			body =[{'text': value}]
			#make request to azure translation service   
			request = requests.post(constructed_url, params=params, headers=headers, json=body)
			response=request.json()
			#print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':')))

			#parse response
			#response as a list of dictionaries
			outFile.write(response[0]['translations'][0]['text'])
		outFile.close()'''
	for fname, content in alerts:
        	body = [{'text': content}]
        	response = requests.post(constructed_url, params=params, headers=headers, json=body)
        	response_json = response.json()

        	backtrans = response_json[0]['translations'][0]['text']
        	out_path = os.path.join(output_dir, fname)
        	with open(out_path, "w", encoding="utf-8") as out_f:
            		out_f.write(backtrans)

def main():
	load_dotenv() #load env variables form .env file
	langs = ["es", "vi", "ko", "km", "so"]

	for lang in langs:
        	input_dir = os.path.join("azure", "forward_translations", lang)
        	alerts = load_alerts(input_dir)
        	translate_text(alerts, lang)
	

if __name__ == "__main__":
	main()

   #.env files create file .env hide this file and put keys in here - put in main
   # define keys key =""
   # from dotenv import load_dotenv
   #  key=os.getenv("AZURE_TRANSLATE_KEY")
   
