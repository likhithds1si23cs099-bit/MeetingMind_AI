"""Download a compact QMSum sample as JSONL for project experimentation."""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", default="data/qmsum_sample.jsonl")
    parser.add_argument("--dataset", default="pszemraj/qmsum-cleaned")
    args = parser.parse_args()

    try:
        from datasets import load_dataset
    except ImportError:
        raise SystemExit("Install dependencies first: pip install -r requirements.txt")

    print(f"Loading dataset: {args.dataset}")
    ds = load_dataset(args.dataset, split="train")
    print("Available columns:", ds.column_names)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with out.open("w", encoding="utf-8") as f:
        for row in ds:
            # The public dataset schema may evolve; retain the raw row as well.
            item = {
                "query": row.get("query", row.get("question", "")),
                "reference_summary": row.get("summary", row.get("answer", "")),
                "transcript": row.get("transcript", row.get("meeting_transcripts", "")),
                "raw": row,
            }
            f.write(json.dumps(item, ensure_ascii=False, default=str) + "\n")
            count += 1
            if count >= args.limit:
                break
    print(f"Saved {count} examples to {out}")

if __name__ == "__main__":
    main()
