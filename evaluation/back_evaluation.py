import os
from comet import download_model, load_from_checkpoint
from sacrebleu import corpus_bleu
from bert_score import score as bert_score
import torch

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
shared_eval_dir = "evaluation"
alert_dir = "data"

comet_model_path = download_model("Unbabel/wmt22-comet-da")
comet_model = load_from_checkpoint(comet_model_path)

def load_combined_alerts():
    alert_path = os.path.join(shared_eval_dir, "combined_alerts.txt")
    with open(alert_path, "r", encoding="utf-8") as f:
        return [line.replace("\n", " ").strip() for line in f.readlines() if line.strip()]

def load_backtranslations(provider, lang):
    bt_path = os.path.join(provider, "back_translations", lang)
    if not os.path.exists(bt_path):
        print(f"Missing backtranslation for {provider} {lang}")
        return []
    
    bt_lines = []
    for filename in sorted(os.listdir(bt_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(bt_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().replace("\n", " ").strip()
                bt_lines.append(content)

    return bt_lines

def load_forward_translations(provider, lang):
    src_path = os.path.join(provider, "forward_translations", lang)
    if not os.path.exists(src_path):
        print(f"Missing forward translations for {provider} {lang}")
        return []

    src_lines = []
    for filename in sorted(os.listdir(src_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(src_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                src_lines.append(f.read().strip())

    return src_lines

def load_bleu_refs_and_bts(provider, lang):
    ref_texts = []
    bt_texts = []
    bt_dir = os.path.join(provider, "back_translations", lang)

    for root, _, files in os.walk(alert_dir):
        for file in sorted(files):
            if not file.endswith(".txt"):
                continue

            alert_path = os.path.join(root, file)
            bt_path = os.path.join(bt_dir, file)

            if not os.path.exists(bt_path):
                print(f"[{provider}][{lang}] Missing backtranslation for: {file}")
                continue

            with open(alert_path, "r", encoding="utf-8") as f:
                ref = f.read().replace("\n", " ").strip()
            with open(bt_path, "r", encoding="utf-8") as f:
                bt = f.read().replace("\n", " ").strip()

            if ref and bt:
                ref_texts.append(ref)
                bt_texts.append(bt)

    return ref_texts, bt_texts

def evaluate_backtranslations(srcs, refs, bts):
    if not (len(srcs) == len(bts) == len(refs)):
        print("Mismatch in line count.")
        return None, None

    # COMET
    comet_data = [{"src": src, "mt": bt, "ref": ref} for src, bt, ref in zip(srcs, bts, refs)]
    device = 1 if torch.cuda.is_available() else 0
    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=device, num_workers=1)
    comet_avg = comet_scores.system_score

    # BERTScore
    P, R, F1 = bert_score(bts, refs, lang="en", rescale_with_baseline=False)
    bert_avg = float(F1.mean())

    return comet_avg, bert_avg

def main():
    ref_lines = load_combined_alerts()
    os.makedirs(shared_eval_dir, exist_ok=True)

    header = f"{'Provider':<10} {'Language':<10} {'COMET':<10} {'BLEU':<10} {'BERTScore':<10}"

    for provider in providers:
        provider_output_path = os.path.join(shared_eval_dir, f"{provider}_back_evaluation_results.txt")
        with open(provider_output_path, "w", encoding="utf-8") as prov_out:
            prov_out.write(header + "\n")

            for lang in langs:
                bt_lines = load_backtranslations(provider, lang)
                src_lines = load_forward_translations(provider, lang)
                bleu_refs, bleu_bts = load_bleu_refs_and_bts(provider, lang)

                combined_out_path = os.path.join(shared_eval_dir, f"{provider}_{lang}_back_combined.txt")
                with open(combined_out_path, "w", encoding="utf-8") as f:
                    for line in bt_lines:
                        f.write(line + "\n")

                print(f"{provider}/{lang} — refs: {len(ref_lines)}, srcs: {len(src_lines)}, bts: {len(bt_lines)}, bleu_refs: {len(bleu_refs)}")

                if not bt_lines or not src_lines or not bleu_refs or not bleu_bts:
                    line = f"{provider:<10} {lang:<10} {'Error':<10} {'Error':<10} {'Error':<10}"
                else:
                    comet_avg, bert = evaluate_backtranslations(src_lines, ref_lines, bt_lines)
                    bleu = corpus_bleu(bleu_bts, [bleu_refs]).score
                    line = f"{provider:<10} {lang:<10} {comet_avg:<10.4f} {bleu:<10.2f} {bert:<10.4f}"

                prov_out.write(line + "\n")

if __name__ == "__main__":
    main()

