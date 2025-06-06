from google.cloud import translate_v2 as translate
import os, json
from dotenv import load_dotenv

#translates text using Neural Machine Translation in Google Cloud Translation API

'''Translate_text function needs to be edited to correctly read in files from folder.
We either need a good way to read in the files from their subdirectories or put all the files 
together in one directory instead of sub directories.

Also, we need to read the names of the input files to make names for the output files. I 
figured it would be easiest to fix all of this once we have the code to read the directory.

'''
  
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
	#initialize translation client, key should be in .env file
	translate_client=translate.Client(key=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_1")) #need to add key and hide .env file

	#new loop to read through alerts dict and translate each file
	for k, value in alerts.items():
		#create new file for each translated file, using category key and lang code
		with open(f"{k}_{lang}.txt", "w") as outFile:    
			translation=translate_client.translate(value, target_language=lang, source_language="en") #should shut off auto lang detection that eats credits
			outFile.write(translation['translatedText'])
	outFile.close()

def main():
	#read in data files from data directory, probably should store the name of the file in var too
	#also need to read in api key from env variable
	#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"
	load_dotenv() #reads in env variables from .env file

	#below needs to be edited to correctly read in the files
	#data_dir = "data" #hardcode actual path to data directory?

	alerts = load_alerts("dummy.txt")
	


	#translate to target languages: 
	translate_text(alerts, "es")	#Spanish translation
	'''translate_text(alerts, "vi")	#Vietnamese translation
	translate_text(alerts, "ko")	#Korean translation	
	translate_text(alerts, "km")	#Khmer translation
	translate_text(alerts, "so")'''	#Somali translation

if __name__ == "__main__":
	main() 
