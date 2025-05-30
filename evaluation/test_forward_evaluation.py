import os
from comet import download_model, load_from_checkpoint
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuest

providers = ["azure", "googlecloud"]
translation_langs = ["es", "vi", "ko", "km", "so"]
alert_dir = "test_data"
shared_eval_dir = "evaluation"

#combine alerts into one file, combine translations into single file per lang
def combine_alerts_for_eval(lang, provider):
    src_texts, mt_texts = [], []
    mt_dir = os.path.join(provider, "test_forward_translations", lang)
    os.makedirs(shared_eval_dir, exist_ok=True)

    for root, _, files in os.walk(alert_dir):
        for file in sorted(files):
            if file.endswith(".txt"):
                src_path = os.path.join(root, file)
                mt_path = os.path.join(mt_dir, file)

                if not os.path.exists(mt_path):
                    print(f"[{provider}]Warning: No translation found for {file} in {lang}")
                    continue

                with open(src_path, "r", encoding="utf-8") as src_f:
                    src_text = src_f.read().strip()
                with open(mt_path, "r", encoding="utf-8") as mt_f:
                    mt_text = mt_f.read().strip()

                src_texts.append(src_text)
                mt_texts.append(mt_text)

    with open(os.path.join(shared_eval_dir, "combined_alerts.txt"), "w", encoding="utf-8") as src_out:
        src_out.write("\n".join(src_texts) + "\n")

    with open(os.path.join(shared_eval_dir, f"{lang}_combined.txt"), "w", encoding="utf-8") as mt_out:
        mt_out.write("\n".join(mt_texts) + "\n")

def evaluate_language(lang, provider, comet_model, mtq_model):
    src_file = os.path.join(shared_eval_dir, "combined_alerts.txt")
    mt_file = os.path.join(shared_eval_dir, f"{provider}_{lang}_combined.txt")

    if not os.path.exists(src_file) or not os.path.exists(mt_file):
        print(f"[{provider}][{lang}] Skipping: Missing combined files.")
        return None

    with open(src_file, "r", encoding="utf-8") as f:
        src_lines = [line.strip() for line in f.readlines()]
    with open(mt_file, "r", encoding="utf-8") as f:
        mt_lines = [line.strip() for line in f.readlines()]

    if len(src_lines) != len(mt_lines):
        print(f"[{provider}][{lang}] Warning: Line count mismatch.")
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

    os.makedirs(shared_eval_dir, exist_ok=True)
    
    for provider in providers:
        print(f"\n=== Evaluating provider: {provider} ===") #remove after test
        results_file = os.path.join(shared_eval_dir, f"{provider}_evaluation_results.txt")
    
        with open(results_file, "w", encoding="utf-8") as f:
            f.write("Language\tCOMET-QE\tMonoTransQuest\n")
            for lang in translation_langs:
                combine_alerts_for_eval(lang, provider)
                result = evaluate_language(lang, provider, comet_model, mtq_model)
                if result:
                    lang, comet_score, mtq_score = result
                    f.write(f"{lang}\t{comet_score:.4f}\t{mtq_score:.4f}\n")
                    print(f"[{provider}][{lang}]: COMET={comet_score:.4f}, MTQ={mtq_score:.4f}")
                else:
                    f.write(f"{lang}\tError\tError\n")


if __name__ == "__main__":
    main()
