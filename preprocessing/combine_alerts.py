import os

#alerts need to be combined into one file and same for translations
def combine_alerts_for_eval(src_dir, mt_dir, out_src_file, out_mt_file):
    src_texts = []
    mt_texts = []

    for file in sorted(os.listdir(src_dir)):
        if file.endswith(".txt"):
            src_path = os.path.join(src_dir, file)
            mt_path = os.path.join(mt_dir, file)

            if not os.path.exists(mt_path):
                print(f"Warning: No translation found for {file}")
                continue

            with open(src_path, "r", encoding="utf-8") as src_f:
                src_text = src_f.read().strip()

            with open(mt_path, "r", encoding="utf-8") as mt_f:
                mt_text = mt_f.read().strip()

            src_texts.append(src_text)
            mt_texts.append(mt_text)

    with open(out_src_file, "w", encoding="utf-8") as src_out:
        for line in src_texts:
            src_out.write(line + "\n")

    with open(out_mt_file, "w", encoding="utf-8") as mt_out:
        for line in mt_texts:
            mt_out.write(line + "\n")

    print(f"Combined {len(src_texts)} alert pairs into {out_src_file} and {out_mt_file}")

if __name__ == "__main__":
    languages = ["es", "vi", "ko", "km", "so"]
    for lang in languages:
        combine_alerts_for_eval(
            src_dir="data/alerts",
            mt_dir=f"data/translations/{lang}",
            out_src_file="preprocessing/combined_alerts.txt",
            out_mt_file=f"preprocessing/{lang}_combined.txt"
        )
