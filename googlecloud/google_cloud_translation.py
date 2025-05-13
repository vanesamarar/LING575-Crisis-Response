from google.cloud import translate_v2 as translate
import os

#translates text using Google Cloud Translation API

'''Translate_text function needs to be edited to correctly read in files from folder.
We either need a good way to read in the files from their subdirectories or put all the files 
together in one directory instead of sub directories.

Also, we need to read the names of the input files to make names for the output files. I 
figured it would be easiest to fix all of this once we have the code to read the directory.

'''

def load_alerts(data_dir):
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
     #Google Cloud Translation API client
     #Not sure if the correct translation model was imported- google documentation not great
     translate_client=translate.Client()       

     #iterate through files and translate each one to target language
     for item in alerts:
         #open each file
         with open("data/%s" % item, "r") as openFile:  #these file reads are not going to work
             data=openFile.read()
             #send to translation
             translation=translate_client.translate(data, target_language=lang, source_language="en") #should shut off auto lang detection that eats credits
             #write to translated text to outfile
             with open("data/%s_%s" % (item, lang), "w") as outFile:  #this probably needs to be changed too
                 outFile.write(translation['translatedText'])
                 print("Translated %s to %s" % (item, lang))
             outFile.close()
         openFile.close()

#new loop to read through alerts dict and translate each file       
'''
    for key, value in alerts.items():
     #create new file for each translated file, using category key and lang code
     with open(f"{key}_{lang}.txt", "w") as outFile:    
          translation=translate_client.translate(value, target_language=lang, source_language="en") #should shut off auto lang detection that eats credits
          outFile.write(translation['translatedText'])
     outFile.close()'''

def main():
    #read in data files from data directory, probably should store the name of the file in var too
    #also need to read in api key from env variable
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"
    #below needs to be edited to correctly read in the files
    data_dir = "data" #need the actual path to data directory


    alerts = load_alerts(data_dir)
    
    #translate to target language
    translate_text(alerts, "es")   #change lang codes as needed
    translate_text(alerts, "es")
    translate_text(alerts, "es")
    translate_text(alerts, "es")
    translate_text(alerts, "es")

if __name__ == "__main__":
    main() 
