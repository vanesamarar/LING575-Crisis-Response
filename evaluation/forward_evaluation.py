import os
from comet import download_model, load_from_checkpoint
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuest

#set up paths and languages
alert_dir = "data"
translation_base_dir = "translations"
combined_dir = "evaluation"
translation_langs = ["es", "vi", "ko", "km", "so"]
results_file = os.path.join(combined_dir, "evaluation_results.txt")
#make sure all directories exist, make them if not
os.makedirs(combined_dir, exist_ok=True)

#combine alerts into one file, combine translations into single file per lang
def combine_alerts_for_eval(lang):
    src_texts, mt_texts = [], []
    src_dir = alert_dir
    mt_dir = os.path.join(translation_base_dir, lang)

    for file in sorted(os.listdir(src_dir)):
        if file.endswith(".txt"):
            src_path = os.path.join(src_dir, file)
            mt_path = os.path.join(mt_dir, file)

            if not os.path.exists(mt_path):
                print(f"Warning: No translation found for {file} in {lang}")
                continue

            with open(src_path, "r", encoding="utf-8") as src_f:
                src_text = src_f.read().strip()
            with open(mt_path, "r", encoding="utf-8") as mt_f:
                mt_text = mt_f.read().strip()

            src_texts.append(src_text)
            mt_texts.append(mt_text)

    with open(os.path.join(combined_dir, "combined_alerts.txt"), "w", encoding="utf-8") as src_out:
        for line in src_texts:
            src_out.write(line + "\n")

    with open(os.path.join(combined_dir, f"{lang}_combined.txt"), "w", encoding="utf-8") as mt_out:
        for line in mt_texts:
            mt_out.write(line + "\n")

def evaluate_language(lang, comet_model, mtq_model):
    src_file = os.path.join(combined_dir, "combined_alerts.txt")
    mt_file = os.path.join(combined_dir, f"{lang}_combined.txt")

    if not os.path.exists(src_file) or not os.path.exists(mt_file):
        print(f"Skipping {lang}: Missing files.")
        return None

    with open(src_file, "r", encoding="utf-8") as f:
        src_lines = [line.strip() for line in f.readlines()]
    with open(mt_file, "r", encoding="utf-8") as f:
        mt_lines = [line.strip() for line in f.readlines()]

    if len(src_lines) != len(mt_lines):
        print(f"Warning: Mismatch in line count for {lang}")
        return None

    comet_data = [{"src": src, "mt": mt} for src, mt in zip(src_lines, mt_lines)]
    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=1 if comet_model.hparams.use_gpu else 0)
    comet_avg = sum(comet_scores) / len(comet_scores)

    mtq_scores, _ = mtq_model.predict(mt_lines, src_lines)
    mtq_scores = list(map(float, mtq_scores))
    mtq_avg = sum(mtq_scores) / len(mtq_scores)

    return lang, comet_avg, mtq_avg

def main():
    comet_model_path = download_model("Unbabel/wmt22-cometkiwi-da")
    comet_model = load_from_checkpoint(comet_model_path)

    mtq_model = MonoTransQuest(model_name_or_path="TransQuest/monotransquest-da-en")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("Language\tCOMET-QE\tMonoTransQuest\n")
        for lang in languages:
            combine_alerts_for_eval(lang)
            result = evaluate_language(lang, comet_model, mtq_model)
            if result:
                lang, comet_score, mtq_score = result
                f.write(f"{lang}\t{comet_score:.4f}\t{mtq_score:.4f}\n")
                print(f"{lang}: COMET={comet_score:.4f}, MTQ={mtq_score:.4f}")
            else:
                f.write(f"{lang}\tError\tError\n")


if __name__ == "__main__":
    main()
