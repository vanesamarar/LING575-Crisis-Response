import os 

def comet_qe(src_file, mt_file):
  with open(src_file, 'r', encoding='utf-8') as f_src, open(mt_file, 'r', encoding='utf-8') as f_mt:
    src_lines = f_src.readlines()
    mt_lines = f_mt.readlines()
  #INSERT COMET-QE LOGIC

def monotransquest(src_file, mt_file):
  with open(src_file, 'r', encoding='utf-8') as f_src, open(mt_file, 'r', encoding='utf-8') as f_mt:
    src_lines = f_src.readlines()
    mt_lines = f_mt.readlines()
  #INSERT MONOTRANSQUEST LOGIC

def main():
  for lang in translation_langs:
        src_file = os.path.join(combined_dir, "combined_alerts.txt")
        mt_file = os.path.join(combined_dir, f"{lang}_combined.txt")

        if not os.path.exists(src_file) or not os.path.exists(mt_file):
            print(f"Missing combined files for language '{lang}'. Please run combine_alerts.py first.")
            continue

        evaluate_translation(src_file, mt_file)


if __name__ == "__main__":
    main()
