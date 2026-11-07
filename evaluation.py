"""ROUGE baseline for JSONL rows containing generated_summary and reference_summary."""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/qmsum_sample.jsonl")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    try:
        from rouge_score import rouge_scorer
    except ImportError:
        raise SystemExit("Install dependencies first: pip install -r requirements.txt")

    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"File not found: {path}. Run dataset_prepare.py first.")

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    totals = {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
    count = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            if count >= args.limit:
                break
            row = json.loads(line)
            pred = row.get("generated_summary", "")
            ref = row.get("reference_summary", "")
            if not pred or not ref:
                continue
            scores = scorer.score(ref, pred)
            for key in totals:
                totals[key] += scores[key].fmeasure
            count += 1

    if not count:
        print("No generated_summary/reference_summary pairs found.")
        print("Generate predictions first and add a generated_summary field to each JSONL row.")
        return
    print(f"Evaluated {count} rows")
    for key, value in totals.items():
        print(f"{key}: {value / count:.4f}")

if __name__ == "__main__":
    main()
