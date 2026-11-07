# MeetingMind AI
**AI Meeting Summarizer, Decision Tracker and Action-Item Agent**

A local-first GenAI student project that turns meeting transcripts into structured reports: summary, key points, decisions, action items, owners, deadlines, open questions, and transcript-grounded Q&A.

## 1. Features
- Modern Streamlit dashboard with dark UI.
- Paste or upload `.txt` meeting transcripts.
- Qwen2.5 through Ollama for local LLM analysis.
- Structured JSON report with Pydantic-ready fields.
- Decision and action-item evidence fields to support verification.
- Ask Meeting Q&A grounded in the transcript.
- Local meeting history and JSON report download.
- Offline rule-based preview if Ollama is unavailable (clearly labelled).
- QMSum dataset preparation and ROUGE evaluation scripts.

## 2. Requirements
- Python 3.10 or newer
- Ollama (for real LLM inference)
- 8 GB RAM recommended; model performance depends on machine resources.

## 3. Run on macOS
Open Terminal in this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Ollama from https://ollama.com/download/mac, then run:

```bash
ollama pull qwen2.5:3b
ollama serve
```

Open a second Terminal tab in the project folder:

```bash
source .venv/bin/activate
streamlit run app.py
```

The browser should open at `http://localhost:8501`.

If the `ollama` command is not found, install Ollama first and reopen Terminal. The app can still launch in offline demo mode, but full AI analysis and Ask Meeting require Ollama.

## 4. How to use
1. Open **Analyze Meeting** from the sidebar.
2. Enter a meeting title.
3. Paste a transcript or upload a `.txt` file.
4. Click **Generate meeting report**.
5. Review Summary, Key decisions, Action items, Open questions, and Verification.
6. Open **Ask Meeting** to ask questions about the transcript.
7. Download the report as JSON.

## 5. Dataset: QMSum
Official repository: https://github.com/Yale-LILY/QMSum  
Hugging Face dataset: https://huggingface.co/datasets/pszemraj/qmsum-cleaned

Prepare a small sample:

```bash
python dataset_prepare.py --limit 1000
```

The script attempts to load the Hugging Face dataset. Dataset schemas can change; inspect the printed columns and update the field mapping if needed.

## 6. Evaluation
After preparing `data/qmsum_sample.jsonl`:

```bash
python evaluation.py --input data/qmsum_sample.jsonl --limit 100
```

The evaluation script computes ROUGE-1/2/L when the dataset rows contain generated and reference summaries. It is a baseline evaluation utility; action-item correctness and factual consistency still require human annotation or a dedicated evaluator.

## 7. Architecture
```text
Transcript / TXT
       |
       v
Preprocessing
       |
       v
Topic & Context Understanding
       |
       +------> Query-focused Q&A
       |
       v
Qwen2.5 via Ollama
       |
       +------> Summary & Key Points
       +------> Decision Extraction
       +------> Action-item Extraction
       +------> Open Questions
       |
       v
Evidence / Consistency Review
       |
       v
Meeting Report + Local History
       |
       v
Streamlit User Interface
```

## 8. MongoDB extension
By default, history is stored locally in `data/meetings.json`, so the app runs without a database server. To enable MongoDB storage, copy `.env.example` to `.env`, set `MONGODB_URI` and `MONGODB_DATABASE`, and restart the app. The app will use the MongoDB collection when it can connect and retain local JSON as a fallback. Do not put database credentials in source code.

## 9. Project limitations and responsible use
- Offline fallback is a simple rule-based preview, not an LLM.
- LLM outputs can contain errors. Verify decisions, owners, and deadlines against transcript evidence.
- The prototype does not automatically send emails, assign tasks, or record meetings.
- Avoid uploading confidential meeting transcripts to services without permission.
