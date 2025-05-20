from google.cloud import translate_v2 as translate
import os

translation_langs = ["es", "vi", "ko", "km", "so"]
input_dir = "data"
output_dir = "translations"

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

def translate_text(alerts, lang, out_dir):
  translate_client = translate.Client()
  lang_dir = os.path.join(out_dir, lang)
  os.makedirs(lang_dir, exist_ok=True)

  for file, content in alerts:
        translation = translate_client.translate(
            content,
            target_language=lang,
            source_language="en"
        )
        out_path = os.path.join(lang_dir, file)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(translation['translatedText'])
        print(f"Translated {file} to {lang}")
