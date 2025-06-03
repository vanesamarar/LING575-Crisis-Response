import os
import torch
from comet import download_model, load_from_checkpoint

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
alert_dir = "data"
shared_eval_dir = "evaluation"

def collect_alert_and_forward_files(provider, lang):
    ref_texts = []
    mt_texts = []
    mt_dir = os.path.join(provider, "forward_translations", lang)

    for root, _, files in os.walk(alert_dir):
        for file in sorted(files):
            if not file.endswith(".txt"):
                continue

            alert_path = os.path.join(root, file)
            mt_path = os.path.join(mt_dir, file)

            if not os.path.exists(mt_path):
                print(f"[{provider}][{lang}] Missing forward translation for: {file}")
                continue

            with open(alert_path, "r", encoding="utf-8") as f:
                ref = f.read().replace("\n", " ").strip()
            with open(mt_path, "r", encoding="utf-8") as f:
                mt = f.read().replace("\n", " ").strip()

            if ref and mt:
                ref_texts.append(ref)
                mt_texts.append(mt)

    return ref_texts, mt_texts

def main():
    comet_model_path = download_model("Unbabel/wmt22-cometkiwi-da")
    comet_model = load_from_checkpoint(comet_model_path)

    os.makedirs(shared_eval_dir, exist_ok=True)
    header = f"{'Provider':<12} {'Language':<10} {'COMET-Kiwi':<12}"

    for provider in providers:
        results_path = os.path.join(shared_eval_dir, f"{provider}_cometkiwi_results.txt")
        with open(results_path, "w", encoding="utf-8") as out_f:
            out_f.write(header + "\n")

            for lang in langs:
                refs, mts = collect_alert_and_forward_files(provider, lang)

                if not refs or not mts or len(refs) != len(mts):
                    print(f"[{provider}][{lang}] Skipping — missing or misaligned data.")
                    line = f"{provider:<12} {lang:<10} {'Error':<12}"
                else:
                    comet_data = [{"src": ref, "mt": mt} for ref, mt in zip(refs, mts)]
                    device = 1 if torch.cuda.is_available() else 0
                    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=device, num_workers=1)
                    comet_avg = comet_scores.system_score
                    line = f"{provider:<12} {lang:<10} {comet_avg:<12.4f}"

                out_f.write(line + "\n")

if __name__ == "__main__":
    main()
