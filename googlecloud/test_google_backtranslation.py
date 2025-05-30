import os, json
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate


#adjust load_alerts to account for directory formatting from forward translation -- see notes in main()
def load_alerts(data_dir):
#load txt files and their contents from data directory and store as list
	alerts = []
	for root, _, files in os.walk(data_dir):
		for file in files:
			if file.endswith(".txt"):
				full_path = os.path.join(root, file)
				with open(full_path, "r", encoding="utf-8") as f:
					content = f.read()
				alerts.append((file, content))
	return alerts
	
def translate_text(alerts, lang):
	#initialize translation client, key should be in .env file -- utilizes second google API key
	translate_client=translate.Client(key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_2")) #need to add key and hide 

	#new loop to read through alerts dict and translate each file
	for k, value in alerts.items():
		#create new file for each translated file, using category key and lang code
		with open(f"{k}_{lang}_en.txt", "w") as outFile:    
			translation=translate_client.translate(value, target_language="en", source_language=lang)
			outFile.write(translation['translatedText'])
	outFile.close()


#main
def main():
	load_dotenv() #reads in env variables from .env file

	#for backtranslation we probably should read each directory and their associated files separately for each language
	data_dir = "data" #hardcode actual path to data directory?
	
    #translate back to English from Spanish; alerts should overwrite/delete previous loaded translations for each load_alerts call
	alerts = load_alerts(data_dir)
	translate_text(alerts, "es")
	
    #translate back to English from Vietnamese
	alerts = load_alerts(data_dir)
	translate_text(alerts, "vi")
	
    #translate back to English from Korean
	alerts=load_alerts(data_dir)
	translate_text(alerts, "ko")
	
    #translate back to English from Khmer
	alerts=load_alerts(data_dir)
	translate_text(alerts, "km")
	
    #translate back to English from Somali
	alerts=load_alerts(data_dir)
	translate_text(alerts, "so")


if __name__ == "__main__":
	main() 
