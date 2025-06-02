import os, json
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import html

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
	translate_client = translate.Client()
	output_dir = os.path.join("googlecloud", "back_translations", lang)
	os.makedirs(output_dir, exist_ok=True)
	
	for fname, content in alerts:
		lines = content.strip().splitlines()
		translations = []

		for line in lines:
			if line.strip() == "":
				translations.append("")
				continue
			translated = translate_client.translate(line, target_language="en", source_language=lang)
			unescaped = html.unescape(translated["translatedText"])
			translations.append(unescaped)

		output_path = os.path.join(output_dir, fname)
		with open(output_path, "w", encoding="utf-8") as outFile:
			outFile.write("\n".join(translations))
			
def main():
	load_dotenv()
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_2")
	langs = ["es", "vi", "ko", "km", "so"]
	for lang in langs:
		input_dir = os.path.join("googlecloud", "forward_translations", lang)
		alerts = load_alerts(input_dir)
		translate_text(alerts, lang)


if __name__ == "__main__":
	main() 
