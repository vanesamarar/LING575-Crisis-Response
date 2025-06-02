import os
from comet import download_model, load_from_checkpoint
from sacrebleu import corpus_bleu
from bert_score import score as bert_score
import torch

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
shared_eval_dir = "evaluation"

comet_model_path = download_model("Unbabel/wmt22-comet-da")
comet_model = load_from_checkpoint(comet_model_path)

def load_combined_alerts():
    alert_path = os.path.join(shared_eval_dir, "combined_alerts.txt")
    with open(alert_path, "r", encoding="utf-8") as f:
        #return [line.strip() for line in f.readlines()]
        return [line.replace("\n", " ").strip() for line in f.readlines() if line.strip()]

def load_backtranslations(provider, lang):
    bt_path = os.path.join(provider, "test_back_translations", lang)
    if not os.path.exists(bt_path):
        print(f"Missing backtranslation for {provider} {lang}")
        return []
    
    bt_lines = []
    for filename in sorted(os.listdir(bt_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(bt_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                #bt_lines.extend([line.strip() for line in f if line.strip()]) THIS
                #bt_lines.append(f.read().strip()) OR THIS 
                content = f.read().replace("\n", " ").strip()
                bt_lines.append(content)

    return bt_lines

def load_forward_translations(provider, lang):
    src_path = os.path.join(provider, "test_forward_translations", lang)
    if not os.path.exists(src_path):
        print(f"Missing forward translations for {provider} {lang}")
        return []

    src_lines = []
    for filename in sorted(os.listdir(src_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(src_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                #src_lines.extend([line.strip() for line in f if line.strip()])
                src_lines.append(f.read().strip())

    return src_lines

def evaluate_backtranslations(srcs, refs, bts):
    if not (len(srcs) == len(bts) == len(refs)):
        print("Mismatch in line count.")
        return None, None, None
    #COMET
    comet_data = [{"src": src, "mt": bt, "ref": ref} for src, bt, ref in zip(srcs, bts, refs)]
    device = 1 if torch.cuda.is_available() else 0
    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=device, num_workers=1)
    comet_avg = comet_scores.system_score
    
    #BLEU
    bleu = corpus_bleu(bts, [refs]).score
    
    #BERTScore
    P, R, F1 = bert_score(bts, refs, lang="en", rescale_with_baseline=True)
    bert_avg = float(F1.mean())

    for i in range(min(3, len(refs))):
        print(f"REF {i} raw repr: {repr(refs[i])}")
        print(f"BT  {i} raw repr: {repr(bts[i])}")

    print("\n--- Sample backtranslation evaluation ---")
    for i in range(min(3, len(refs))):
        print(f"REF {i}: {refs[i]}")
        print(f"BT  {i}: {bts[i]}")
    print("--- End sample ---\n")

    return comet_avg, bleu, bert_avg
    
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

                combined_out_path = os.path.join(shared_eval_dir, f"{provider}_{lang}_back_combined.txt")
                with open(combined_out_path, "w", encoding="utf-8") as f:
                    for line in bt_lines:
                        f.write(line + "\n")

                print(f"{provider}/{lang} — refs: {len(ref_lines)}, srcs: {len(src_lines)}, bts: {len(bt_lines)}")

                if not bt_lines or not src_lines:
                    line = f"{provider:<10} {lang:<10} {'Error':<10} {'Error':<10} {'Error':<10}"
                else:
                    comet_avg, bleu, bert = evaluate_backtranslations(src_lines, ref_lines, bt_lines)
                    if comet_avg is None:
                        line = f"{provider:<10} {lang:<10} {'Error':<10} {'Error':<10} {'Error':<10}"
                    else:
                        line = f"{provider:<10} {lang:<10} {comet_avg:<10.4f} {bleu:<10.2f} {bert:<10.4f}"

                prov_out.write(line + "\n")

if __name__ == "__main__":
    main()
    main()
