import os
from comet import download_model, load_from_checkpoint
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuest

translation_langs = ["es", "vi", "ko", "km", "so"]

#load COMET-QE
comet_model_path = download_model("wmt21-comet-qe-da")
comet_model = load_from_checkpoint(comet_model_path)

#load MonoTransQuest
transquest_model = MonoTransQuest("TransQuest/monotransquest-da-en_XX-wiki")

def comet_qe(src_file, mt_file):
  with open(src_file, 'r', encoding='utf-8') as f_src, open(mt_file, 'r', encoding='utf-8') as f_mt:
    src_lines = [line.strip() for line in f_src]
    mt_lines = [line.strip() for line in f_mt]

  data =  [{"src": src, "mt": mt} for src, mt in zip(src_lines, mt_lines)]
  comet_scores = comet_model.predict(data, batch_size=8, gpus=1)
  print(f"  COMET-QE Average Score: {sum(comet_scores['scores']) / len(comet_scores['scores']):.4f}")

def monotransquest(src_file, mt_file):
  with open(src_file, 'r', encoding='utf-8') as f_src, open(mt_file, 'r', encoding='utf-8') as f_mt:
    src_lines = [line.strip() for line in f_src]
    mt_lines = [line.strip() for line in f_mt]

  predictions = transquest_model.predict(mt_lines, src_lines)
  print(f"  MonoTransQuest Average Score: {sum(predictions) / len(predictions):.4f}")

def evaluate_translation(src_file, mt_file, lang):
  print(f"\nEvaluating forward translation for '{lang}'...")
  comet_qe(src_file, mt_file)
  monotransquest(src_file, mt_file)

def main():
  for lang in translation_langs:
        src_file = os.path.join(combined_dir, "combined_alerts.txt")
        mt_file = os.path.join(combined_dir, f"{lang}_combined.txt")

        if not os.path.exists(src_file) or not os.path.exists(mt_file):
            print(f"Missing combined files for language '{lang}'. Please run combine_alerts.py first.")
            continue

        evaluate_translation(src_file, mt_file, lang)


if __name__ == "__main__":
    main()
