import os
from comet import download_model, load_from_checkpoint
import torch

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
shared_eval_dir = "evaluation"
data_dir = "data"

comet_model_path = download_model("Unbabel/wmt22-comet-da")
comet_model = load_from_checkpoint(comet_model_path)

def collect_files(provider, lang):
    srcs, refs, bts = [], [], []

    bt_dir = os.path.join(provider, "back_translations", lang)
    fwd_dir = os.path.join(provider, "forward_translations", lang)

    if not os.path.exists(bt_dir):
        print(f"Missing back-translations: {bt_dir}")
        return [], [], []

    for filename in sorted(os.listdir(bt_dir)):
        if not filename.endswith(".txt"):
            continue

        alert_path = find_alert_path(filename)
        fwd_path = os.path.join(fwd_dir, filename)
        bt_path = os.path.join(bt_dir, filename)

        if not (os.path.exists(alert_path) and os.path.exists(fwd_path)):
            print(f"Missing file for {filename} — skipping")
            continue

        with open(alert_path, "r", encoding="utf-8") as f:
            ref = f.read().replace("\n", " ").strip()
        with open(fwd_path, "r", encoding="utf-8") as f:
            src = f.read().replace("\n", " ").strip()
        with open(bt_path, "r", encoding="utf-8") as f:
            bt = f.read().replace("\n", " ").strip()

        refs.append(ref)
        srcs.append(src)
        bts.append(bt)

    return srcs, refs, bts

def find_alert_path(filename):
    # Loop over categories to find matching alert
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        if not os.path.isdir(category_path):
            continue

        file_path = os.path.join(category_path, filename)
        if os.path.exists(file_path):
            return file_path

    return None

def evaluate_comet(srcs, refs, bts):
    if not (len(srcs) == len(bts) == len(refs)):
        print("Line mismatch")
        return None

    data = [{"src": src, "mt": bt, "ref": ref} for src, bt, ref in zip(srcs, bts, refs)]
    device = 1 if torch.cuda.is_available() else 0
    scores = comet_model.predict(data, batch_size=8, gpus=device, num_workers=1)
    return scores.system_score

def main():
    os.makedirs(shared_eval_dir, exist_ok=True)
    header = f"{'Provider':<10} {'Language':<10} {'COMET':<10}"

    for provider in providers:
        out_path = os.path.join(shared_eval_dir, f"{provider}_comet_only_results.txt")
        with open(out_path, "w", encoding="utf-8") as out_file:
            out_file.write(header + "\n")

            for lang in langs:
                srcs, refs, bts = collect_files(provider, lang)
                print(f"{provider}/{lang}: {len(refs)} refs, {len(srcs)} srcs, {len(bts)} bts")

                if not srcs or not refs or not bts:
                    out_file.write(f"{provider:<10} {lang:<10} {'Error':<10}\n")
                    continue

                score = evaluate_comet(srcs, refs, bts)
                if score is None:
                    out_file.write(f"{provider:<10} {lang:<10} {'Error':<10}\n")
                else:
                    out_file.write(f"{provider:<10} {lang:<10} {score:<10.4f}\n")

if __name__ == "__main__":
    main()

