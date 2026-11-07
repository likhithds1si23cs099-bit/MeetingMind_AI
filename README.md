# MeetingMind AI
### AI Meeting Summarizer, Decision Tracker & Action-Item Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LLM-Qwen2.5-7C3AED?style=for-the-badge" alt="Qwen2.5"/>
  <img src="https://img.shields.io/badge/Inference-Ollama-111827?style=for-the-badge" alt="Ollama"/>
</p>

A local-first GenAI student project that transforms meeting transcripts into structured, reviewable outputs: summaries, key points, decisions, action items, owners, deadlines, open questions and transcript-grounded Q&A.

## ✨ Features

- 🌙 Streamlit dashboard with a dark interface.
- 📄 Paste a transcript or upload a `.txt` file.
- 🧠 Run local Qwen2.5 inference through Ollama.
- 📝 Generate structured meeting summaries and key points.
- ✅ Extract decisions, action items, owners and deadlines.
- 🔎 Review evidence fields to help verify extracted information.
- 💬 Ask questions grounded in the supplied transcript.
- 💾 Keep local meeting history and download reports as JSON.
- 📴 Use a clearly labelled rule-based preview when Ollama is unavailable.
- 📊 Prepare QMSum samples and run baseline ROUGE evaluation.

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| User interface | Streamlit |
| Local LLM runtime | Ollama |
| Model | Qwen2.5 |
| Structured data | Pydantic-ready report fields |
| Optional database | MongoDB |
| Evaluation | QMSum, ROUGE |

## 🖥️ Requirements

- Python 3.10 or newer
- Ollama for full local LLM inference
- 8 GB RAM recommended; performance depends on the selected model and machine

## ⚙️ Setup on macOS

Clone the repository and open its folder:

```bash
git clone https://github.com/likhithds1si23cs099-bit/MeetingMind_AI.git
cd MeetingMind_AI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Ollama from [ollama.com/download](https://ollama.com/download), then download the model:

```bash
ollama pull qwen2.5:3b
ollama serve
```

Open a second terminal in the project folder, activate the environment and run:

```bash
source .venv/bin/activate
streamlit run app.py
```

The app should open at **http://localhost:8501**.

## 🧭 How to use

1. Open **Analyze Meeting** in the sidebar.
2. Enter a meeting title.
3. Paste the transcript or upload a `.txt` file.
4. Select **Generate meeting report**.
5. Review the summary, decisions, action items, open questions and verification details.
6. Open **Ask Meeting** to ask questions about the transcript.
7. Download the report as JSON when finished.

## 🏗️ Workflow

```text
Meeting transcript / TXT upload
             |
             v
     Text preprocessing
             |
             v
  Local Qwen2.5 via Ollama
             |
     +-------+--------+
     |       |        |
   Summary Decisions Action items
     |       |        |
     +-------+--------+
             |
             v
   Evidence / consistency review
             |
             v
  Report + transcript-grounded Q&A
             |
             v
       Streamlit interface
```

## 📚 Dataset & Evaluation

The repository includes scripts for preparing a QMSum sample and running a baseline ROUGE evaluation.

Dataset sources:
- [QMSum project](https://github.com/Yale-LILY/QMSum)
- [QMSum on Hugging Face](https://huggingface.co/datasets/pszemraj/qmsum-cleaned)

Prepare a sample:

```bash
python dataset_prepare.py --limit 1000
```

Run evaluation:

```bash
python evaluation.py --input data/qmsum_sample.jsonl --limit 100
```

ROUGE is a summary-overlap baseline; it does not establish that extracted owners, decisions or deadlines are correct. Those require additional evaluation.

## 🗄️ Optional MongoDB

By default, meeting history is stored locally in `data/meetings.json`. To use MongoDB, copy `.env.example` to `.env`, configure `MONGODB_URI` and `MONGODB_DATABASE`, then restart the app. Keep credentials out of Git.

## ⚠️ Limitations & Responsible Use

- The offline fallback is a rule-based preview, not an LLM response.
- LLM-generated decisions, owners and deadlines can be incorrect; verify them against the transcript.
- This prototype does not automatically send emails, assign tasks or record meetings.
- Do not upload confidential meeting transcripts to services without permission.

---

<p align="center"><b>Turn conversations into clear next steps.</b></p>
