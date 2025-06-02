from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import os
import html

translation_langs = ["es", "vi", "ko", "km", "so"]
input_dir = "data"
output_dir = "googlecloud/forward_translations"

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
	translate_client = translate.Client()
	lang_dir = os.path.join(out_dir, lang)
	os.makedirs(lang_dir, exist_ok=True)

	for file, content in alerts:
		lines = content.strip().splitlines()
		translations = []

		for line in lines:
			if line.strip() == "":
				translations.append("")
				continue
			translated = translate_client.translate(line, target_language=lang, source_language="en")
			unescaped = html.unescape(translated['translatedText'])
			translations.append(unescaped)

		out_path = os.path.join(lang_dir, file)
		with open(out_path, "w", encoding="utf-8") as f:
			f.write("\n".join(translations))

def main():
	load_dotenv()
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
	alerts = load_alerts(input_dir)

	for lang in translation_langs:
		translate_text(alerts, lang, output_dir)

if __name__ == "__main__":
	main()
