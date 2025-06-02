import os
from sacrebleu import sentence_bleu

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
shared_eval_dir = "evaluation"
output_file = os.path.join(shared_eval_dir, "bleu_per_alert_results.txt")

def load_combined_alerts():
    alert_path = os.path.join(shared_eval_dir, "combined_alerts.txt")
    with open(alert_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_backtranslations(provider, lang):
    bt_path = os.path.join(provider, "back_translations", lang)
    if not os.path.exists(bt_path):
        print(f"Missing backtranslation for {provider} {lang}")
        return [], []

    bt_lines = []
    filenames = []
    for filename in sorted(os.listdir(bt_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(bt_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().replace("\n", " ").strip()
                bt_lines.append(content)
                filenames.append(filename)
    return bt_lines, filenames

def main():
    refs = load_combined_alerts()

    if not os.path.exists(shared_eval_dir):
        os.makedirs(shared_eval_dir)

    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(f"{'Provider':<10}\t{'Language':<5}\t{'AlertFile':<30}\t{'BLEU':>6}\n")

        for provider in providers:
            for lang in langs:
                bts, filenames = load_backtranslations(provider, lang)

                if not bts:
                    continue

                if len(bts) != len(refs):
                    print(f"WARNING: Count mismatch for {provider} {lang}: backtranslations={len(bts)}, refs={len(refs)}")
                    # Just take min length to avoid index error:
                    n = min(len(bts), len(refs))
                else:
                    n = len(bts)

                for i in range(n):
                    score = sentence_bleu(bts[i], [refs[i]]).score
                    out_f.write(f"{provider:<10}\t{lang:<5}\t{filenames[i]:<30}\t{score:6.2f}\n")

    print(f"BLEU per alert results saved to {output_file}")

if __name__ == "__main__":
    main()

