import os
from comet import download_model, load_from_checkpoint
from sacrebleu import corpus_bleu
from bert_score import score as bert_score

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
alert_path = "evaluation/combined_alerts.txt"
output_path = "evaluation/backward_eval_results.txt"
base_dir = os.path.dirname(os.path.abspath(__file__)) #might fix path issue?

comet_model_path = download_model("Unbabel/wmt22-comet-da")
comet_model = load_from_checkpoint(comet_model_path)

def load_combined_alerts():
    alert_path = os.path.join(base_dir, "combined_alerts.txt")
    with open(alert_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]
        
def load_backtranslations(provider, lang):
    bt_path = os.path.join(base_dir, "..", provider, "back_translations", f"{lang}.txt")
    if not os.path.exists(bt_path):
        print(f"Missing backtranslation for {provider} {lang}")
        return []
    with open(bt_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def evaluate_backtranslations(refs, bts):
    if len(refs) != len(bts):
        print("Mismatch in line count.")
        return None, None, None
    #COMET
    comet_data = [{"src": ref, "mt": bt} for ref, bt in zip(refs, bts)]
    comet_scores = comet_model.predict(comet_data, batch_size=8, gpus=1 if comet_model.hparams.use_gpu else 0)
    comet_avg = sum(comet_scores) / len(comet_scores)
    
    #BLEU
    bleu = corpus_bleu(bts, [refs]).score
    
    #BERTScore
    P, R, F1 = bert_score(bts, refs, lang="en", rescale_with_baseline=True)
    bert_avg = float(F1.mean())

    return comet_avg, bleu, bert_avg
    
def main():
    ref_lines = load_combined_alerts()
    output_path = os.path.join(base_dir, "backward_eval_results.txt")

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("Provider\tLanguage\tCOMET\tBLEU\tBERTScore\n")
            
        for provider in providers:
            for lang in langs:
                bt_lines = load_backtranslations(provider, lang)
                if not bt_lines:
                    out_f.write(f"{provider}\t{lang}\tError\tError\tError\n")
                    continue

                combined_bt_path = os.path.join(base_dir, f"back_{provider}_{lang}_combined.txt")
                with open(combined_bt_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(bt_lines) + "\n")
                    
                comet_avg, bleu, bert = evaluate_backtranslations(ref_lines, bt_lines)
                if comet_avg is None:
                    out_f.write(f"{provider}\t{lang}\tError\tError\tError\n")
                else:
                    out_f.write(f"{provider}\t{lang}\t{comet_avg:.4f}\t{bleu:.2f}\t{bert:.4f}\n")
                    print(f"{provider}/{lang}: COMET={comet_avg:.4f}, BLEU={bleu:.2f}, BERT={bert:.4f}")
if __name__ == "__main__":
    main()
