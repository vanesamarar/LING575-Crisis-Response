import os
from sacrebleu import corpus_bleu

providers = ["azure", "googlecloud"]
langs = ["es", "vi", "ko", "km", "so"]
alert_dir = "data"
shared_eval_dir = "evaluation"

def collect_alert_and_bt_files(provider, lang):
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

def main():
    os.makedirs(shared_eval_dir, exist_ok=True)

    header = f"{'Provider':<12} {'Language':<10} {'BLEU':<10}"

    for provider in providers:
        results_path = os.path.join(shared_eval_dir, f"{provider}_bleu_only_results.txt")
        with open(results_path, "w", encoding="utf-8") as out_f:
            out_f.write(header + "\n")

            for lang in langs:
                refs, bts = collect_alert_and_bt_files(provider, lang)

                if not refs or not bts or len(refs) != len(bts):
                    print(f"[{provider}][{lang}] Skipping — missing or misaligned data.")
                    line = f"{provider:<12} {lang:<10} {'Error':<10}"
                else:
                    bleu_score = corpus_bleu(bts, [refs]).score
                    line = f"{provider:<12} {lang:<10} {bleu_score:<10.2f}"

                out_f.write(line + "\n")

if __name__ == "__main__":
    main()

