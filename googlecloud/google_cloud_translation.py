from google.cloud import translate_v2 as translate
import os

#translates text using Google Cloud Translation API

'''Translate_text function needs to be edited to correctly read in files from folder.
We either need a good way to read in the files from their subdirectories or put all the files 
together in one directory instead of sub directories.

Also, we need to read the names of the input files to make names for the output files. I 
figured it would be easiest to fix all of this once we have the code to read the directory.

'''

def translate_text(files, lang):
     #Google Cloud Translation API client
    #Not sure if the correct translation model was imported- google documentation not great
     translate_client=translate.Client()       

     #iterate through files and translate each one to target language
     for item in files:
         #open each file
         with open("data/%s" % item, "r") as openFile:  #these file reads are not going to work
             data=openFile.read()
             #send to translation
             translation=translate_client.translate(data, target_language=lang)
             #write to translated text to outfile
             with open("data/%s_%s" % (item, lang), "w") as outFile:  #this probably needs to be changed too
                 outFile.write(translation['translatedText'])
                 print("Translated %s to %s" % (item, lang))
             outFile.close()
         openFile.close()

def main():
    #read in data files from data directory, probably should store the name of the file in var too

    #below needs to be edited to correctly read in the files
    files=os.listdir("data")
    translate_text(files, "es")   #change lang codes as needed
    translate_text(files, "es")
    translate_text(files, "es")
    translate_text(files, "es")
    translate_text(files, "es")


if __name__=="__main__":
    main()