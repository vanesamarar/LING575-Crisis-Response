import os
from comet import download_model, load_from_checkpoint
from sacrebleu import corpus_bleu
from bert_score import score as bert_score

translation_langs = ["es", "vi", "ko", "km", "so"]
providers = ["azure", "googlecloud"]

eval_dir = "evaluation"
os.makedirs(eval_dir, exist_ok=True)

ef evaluate_backtranslations(provider):
    provider_translation_dir = os.path.join(provider, "backtranslations")
    provider_eval_dir = os.path.join(provider, "evaluation")
    os.makedirs(provider_eval_dir, exist_ok=True)

    combined_ref_file = os.path.join(provider_eval_dir, "combined_alerts.txt")
    if not os.path.exists(combined_ref_file):
        print(f"Missing {combined_ref_file}, skipping {provider}.")
        return

    references = load_lines(combined_ref_file)

    with open(os.path.join(eval_dir, f"{provider}_backward.txt"), "w", encoding="utf-8") as result_file:
        result_file.write("Language\tCOMET\tBLEU\tBERTScore\n")

        for lang in translation_langs:
            back_file = os.path.join(provider_translation_dir, f"{lang}_back.txt")
            if not os.path.exists(back_file):
                print(f"Missing backtranslation for {lang} in {provider}, skipping.")
                result_file.write(f"{lang}\tMissing\tMissing\tMissing\n")
                continue

            backtranslations = load_lines(back_file)

            if len(references) != len(backtranslations):
                print(f"Mismatch in line count for {lang} in {provider}, skipping.")
                result_file.write(f"{lang}\tLengthMismatch\tLengthMismatch\tLengthMismatch\n")
                continue
              
            #ADD COMET LOGIC 

            #ADD BLEU LOGIC

            #ADD BERTSCORE LOGIC

def main():
    for provider in providers:
        evaluate_backtranslations(provider)

if __name__ == "__main__":
    main()
