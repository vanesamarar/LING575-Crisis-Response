from google.cloud import translate_v2 as translate
import os

#translates text using Neural Machine Translation in Google Cloud Translation API

'''Translate_text function needs to be edited to correctly read in files from folder.
We either need a good way to read in the files from their subdirectories or put all the files 
together in one directory instead of sub directories.

Also, we need to read the names of the input files to make names for the output files. I 
figured it would be easiest to fix all of this once we have the code to read the directory.

'''

def load_alerts(data_dir): #change to ignore the subdirectories, pick best container 
#load txt files from data directory and its subdirectories as a dict
	alerts = {}
	for root, _, files in os.walk(data_dir):
		for file in files:
			if file.endswith(".txt"):
				category = os.path.basename(root)
				fpath = os.path.join(root, file)

				with open(fpath, "r", encoding="utf-8") as f:
					content = f.read().strip()

				if category not in alerts:
					alerts[category] = []
				alerts[category].append((file, content))
	return alerts    

def translate_text(alerts, lang):
	#initialize translation client
	translate_client=translate.Client()

	#new loop to read through alerts dict and translate each file
	for key, value in alerts.items():
		#create new file for each translated file, using category key and lang code
		with open(f"{key}_{lang}.txt", "w") as outFile:    
			translation=translate_client.translate(value, target_language=lang, source_language="en") #should shut off auto lang detection that eats credits
			outFile.write(translation['translatedText'])
	outFile.close()

def main():
	#read in data files from data directory, probably should store the name of the file in var too
	#also need to read in api key from env variable
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"
	
	#below needs to be edited to correctly read in the files
	data_dir = "data" #hardcode actual path to data directory?

	alerts = load_alerts(data_dir)
	
	#translate to target languages: 
	translate_text(alerts, "es")	#Spanish translation
	translate_text(alerts, "vi")	#Vietnamese translation
	translate_text(alerts, "ko")	#Korean translation	
	translate_text(alerts, "km")	#Khmer translation
	translate_text(alerts, "so")	#Somali translation

if __name__ == "__main__":
	main() 
