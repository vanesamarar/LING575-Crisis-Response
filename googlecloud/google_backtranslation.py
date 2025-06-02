import os, json
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate


#adjust load_alerts to account for directory formatting from forward translation -- see notes in main()
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
	#initialize translation client, key should be in .env file -- utilizes second google API key
	translate_client=translate.Client(key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_2")) #need to add key and hide 

	output_dir = os.path.join("googlecloud", "back_translations", lang)
	os.makedirs(output_dir, exist_ok=True)
	#new loop to read through alerts dict and translate each file
	for k, value in alerts.items():
		#create new file for each translated file, using category key and lang code
		'''with open(f"{k}_{lang}_en.txt", "w") as outFile:    
			translation=translate_client.translate(value, target_language="en", source_language=lang)
			outFile.write(translation['translatedText'])
	outFile.close()'''
		translated = translate_client.translate(value, target_language="en", source_language=lang)
        	output_path = os.path.join(output_dir, k)
        	with open(output_path, "w", encoding="utf-8") as outFile:
            		outFile.write(translated["translatedText"])



#main
def main():
	load_dotenv() #reads in env variables from .env file

	langs = ["es", "vi", "ko", "km", "so"]
    	for lang in langs:
        	input_dir = os.path.join("googlecloud", "forward_translations", lang)
        	alerts = load_alerts(input_dir)
        	translate_text(alerts, lang)


if __name__ == "__main__":
	main() 
