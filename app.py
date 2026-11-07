import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "meetings.json"

st.set_page_config(
    page_title="MeetingMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling ---------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#eaf0ff; --muted:#9aa8c7; --panel:#111b31; --line:rgba(160,180,220,.14); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(circle at 10% 0%, #1b2c50 0, #0a1222 42%, #080e1b 100%); color:var(--ink); }
header[data-testid="stHeader"] { background:transparent; }
.block-container { padding-top:1.6rem; padding-bottom:3rem; max-width:1440px; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.5px; }
h1 { color:#f5f7ff; }
p, label, .stMarkdown { color:#dce5fa; }
[data-testid="stSidebar"] { background:rgba(10,18,34,.96); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#dce5fa; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(28,43,72,.95),rgba(16,27,48,.95)); border:1px solid var(--line); padding:17px 18px; border-radius:16px; }
div[data-testid="stMetric"] label { color:#9eafd0 !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#fff !important; font-family:'Space Grotesk'; }
.stButton > button { border-radius:11px; border:1px solid rgba(120,151,255,.35); background:linear-gradient(110deg,#6378ef,#8b5cf6); color:white; font-weight:700; padding:.58rem 1rem; }
.stButton > button:hover { border-color:#a9b7ff; color:white; box-shadow:0 8px 24px rgba(99,120,239,.25); }
.stTextArea textarea, .stTextInput input { background:#101b30 !important; color:#eaf0ff !important; border:1px solid #2a3a5b !important; border-radius:12px !important; }
[data-testid="stFileUploader"] { background:rgba(17,27,49,.7); border:1px dashed #53658e; border-radius:14px; padding:12px; }
.panel { background:linear-gradient(145deg,rgba(20,33,58,.96),rgba(13,23,42,.96)); border:1px solid var(--line); border-radius:18px; padding:20px 22px; margin:8px 0 16px 0; box-shadow:0 12px 35px rgba(0,0,0,.12); }
.hero { background:linear-gradient(115deg,rgba(68,91,190,.35),rgba(112,72,190,.20)),#111d35; border:1px solid rgba(143,159,255,.24); border-radius:22px; padding:26px 30px; margin-bottom:22px; }
.eyebrow { color:#9fb0ff; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:700; }
.hero-title { font-family:'Space Grotesk'; font-size:32px; font-weight:700; color:#fff; margin:5px 0; }
.hero-sub { color:#aebcda; font-size:14px; }
.pill { display:inline-block; padding:5px 10px; margin:3px 4px 3px 0; border-radius:20px; font-size:11px; color:#c8d4ff; background:rgba(110,130,255,.14); border:1px solid rgba(130,150,255,.22); }
.small-muted { color:#93a3c4; font-size:12px; }
.section-title { font-family:'Space Grotesk'; color:#f4f6ff; font-size:19px; font-weight:700; margin:8px 0 12px; }
.decision { border-left:3px solid #8b7cff; padding:9px 13px; background:rgba(139,124,255,.08); border-radius:0 10px 10px 0; margin:8px 0; }
.task { border:1px solid var(--line); background:rgba(22,35,60,.72); border-radius:12px; padding:12px 14px; margin:8px 0; }
.question { border-left:3px solid #e6ad62; padding:9px 13px; background:rgba(230,173,98,.08); border-radius:0 10px 10px 0; margin:8px 0; }
hr { border-color:var(--line) !important; }

/* MeetingMind AI — refined responsive dashboard */
:root{--accent:#67e8f9;--violet:#a78bfa;--panel:#111d34;--line:rgba(148,174,220,.18)}
.stApp{background:radial-gradient(ellipse at 12% 0%,rgba(59,130,246,.18),transparent 34%),radial-gradient(ellipse at 88% 8%,rgba(139,92,246,.13),transparent 30%),linear-gradient(145deg,#070d19 0%,#0b1426 55%,#0a1020 100%)}
.block-container{max-width:1500px;padding-top:2rem;padding-bottom:4rem}
.hero{position:relative;overflow:hidden;background:linear-gradient(115deg,rgba(37,99,235,.24),rgba(124,58,237,.18)),linear-gradient(135deg,#142440,#101a31);border:1px solid rgba(103,232,249,.2);border-radius:26px;padding:34px 36px;margin:0 0 28px;box-shadow:0 22px 65px rgba(0,0,0,.22)}
.hero:after{content:"✦";position:absolute;right:7%;top:8%;font-size:110px;color:rgba(103,232,249,.08);font-weight:700;pointer-events:none}
.eyebrow{color:#67e8f9;font-size:11px;letter-spacing:2.8px}
.hero-title{font-size:clamp(27px,4vw,42px);line-height:1.12;letter-spacing:-1.4px;margin:10px 0 12px}
.hero-sub{font-size:15px;max-width:720px;line-height:1.7}
.pill{padding:6px 12px;border-radius:999px;background:rgba(103,232,249,.08);border-color:rgba(103,232,249,.22);color:#b9f4ff}
.panel{border-radius:20px;padding:24px;background:linear-gradient(145deg,rgba(20,35,61,.96),rgba(12,22,40,.96));box-shadow:0 16px 42px rgba(0,0,0,.16)}
.section-title{font-size:21px}
div[data-testid="stMetric"]{min-height:116px;display:flex;flex-direction:column;justify-content:center;border-radius:18px;background:linear-gradient(145deg,rgba(25,44,76,.98),rgba(14,26,47,.98));border:1px solid rgba(103,232,249,.14);box-shadow:0 12px 30px rgba(0,0,0,.13)}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{font-size:30px}
.stButton>button{border-radius:12px;min-height:43px;background:linear-gradient(110deg,#2563eb,#7c3aed);border:1px solid rgba(165,180,252,.35);box-shadow:0 8px 22px rgba(79,70,229,.2);transition:all .18s ease}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgba(79,70,229,.32);border-color:#67e8f9}
.stTextInput input,.stTextArea textarea{border-radius:13px!important;background:#0d192d!important;border:1px solid #2b4164!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:#67e8f9!important;box-shadow:0 0 0 3px rgba(103,232,249,.12)!important}
[data-testid="stFileUploader"]{border-radius:16px;background:rgba(18,31,54,.65);border:1px dashed rgba(103,232,249,.4)}
[data-testid="stTabs"] button{border-radius:10px 10px 0 0;font-weight:600}
.decision,.task,.question{border-radius:13px;padding:14px 16px;margin:10px 0;background:rgba(19,35,60,.75);border:1px solid rgba(148,174,220,.13)}
.decision{border-left:4px solid #a78bfa}.task{border-left:4px solid #22d3ee}.question{border-left:4px solid #fbbf24}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#080f1e,#0d1930);border-right:1px solid rgba(148,174,220,.14)}
[data-testid="stSidebar"] .stRadio label{padding:5px 0}
hr{margin:1.4rem 0!important}
@media(max-width:700px){.block-container{padding:1rem 1rem 3rem}.hero{padding:24px 20px}.hero:after{font-size:68px;right:4%}.hero-title{font-size:28px}}

</style>
""", unsafe_allow_html=True)

# ----------------------------- Helpers ---------------------------------
def _mongo_collection():
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=1200)
        client.admin.command("ping")
        database = os.getenv("MONGODB_DATABASE", "meetingmind")
        return client[database]["meetings"]
    except Exception:
        return None

def load_history():
    collection = _mongo_collection()
    if collection is not None:
        try:
            rows = list(collection.find({}, {"_id": 0}).sort("created_at", -1).limit(100))
            if rows:
                return rows
        except Exception:
            pass
    try:
        return json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.exists() else []
    except Exception:
        return []

def save_history(items):
    safe_items = items[:100]
    HISTORY_FILE.write_text(json.dumps(safe_items, indent=2, ensure_ascii=False))
    collection = _mongo_collection()
    if collection is not None:
        try:
            collection.delete_many({})
            if safe_items:
                collection.insert_many(safe_items)
        except Exception:
            pass

def parse_json_response(raw):
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        raw = raw[start:end+1]
    return json.loads(raw)

def ollama_generate(prompt, model, base_url):
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
        timeout=240,
    )
    response.raise_for_status()
    return response.json().get("response", "")

def fallback_analysis(transcript):
    """Transparent offline demo fallback. Replace with Ollama output for real LLM analysis."""
    lines = [re.sub(r"\s+", " ", x).strip() for x in transcript.splitlines() if x.strip()]
    summary = " ".join(lines[:5])[:900] or "No transcript content was provided."
    decisions, actions, questions = [], [], []
    for line in lines:
        low = line.lower()
        if any(k in low for k in ["decided", "decision", "agreed", "approved", "will proceed", "finalized"]):
            decisions.append({"decision": line, "reason": "Extracted from the meeting transcript.", "participants": "Not explicitly identified"})
        if any(k in low for k in ["action:", "todo:", "to-do:", "will ", "should ", "assigned to", "owner:"]):
            owner = "Not specified"
            m = re.search(r"(?:owner|assigned to)\s*[:\-]?\s*([A-Z][\w .-]+)", line, re.I)
            if m: owner = m.group(1).strip()
            actions.append({"task": line, "owner": owner, "deadline": "Not specified", "status": "Open", "evidence": line})
        if "?" in line or any(k in low for k in ["unresolved", "open question", "pending clarification"]):
            questions.append(line)
    return {
        "meeting_title": "Meeting analysis",
        "summary": summary,
        "key_points": lines[:6],
        "decisions": decisions[:8],
        "action_items": actions[:12],
        "open_questions": questions[:8],
        "overall_status": "Review required",
        "verification_notes": ["Offline demo mode was used. Run Ollama with Qwen2.5 for AI extraction.", "Confirm owners and deadlines against the original transcript."]
    }

def analyze_meeting(transcript, model, base_url):
    prompt = f"""
You are MeetingMind AI, a careful enterprise meeting analyst.
Analyze the transcript. Never invent a person, decision, deadline, or task.
If a field is not stated, write "Not specified". Keep every item traceable to transcript evidence.
Return ONLY valid JSON matching this schema:
{{
 "meeting_title": "short title",
 "summary": "concise 3-6 sentence summary",
 "key_points": ["..."],
 "decisions": [{{"decision":"...", "reason":"...", "participants":"...", "evidence":"exact short supporting quote"}}],
 "action_items": [{{"task":"...", "owner":"...", "deadline":"...", "status":"Open", "evidence":"exact short supporting quote"}}],
 "open_questions": ["..."],
 "overall_status": "On track | At risk | Review required",
 "verification_notes": ["uncertainties or unsupported fields"]
}}
Transcript:
{transcript[:30000]}
"""
    raw = ollama_generate(prompt, model, base_url)
    result = parse_json_response(raw)
    for key, default in [("key_points", []), ("decisions", []), ("action_items", []), ("open_questions", []), ("verification_notes", [])]:
        if not isinstance(result.get(key), list): result[key] = default
    result.setdefault("meeting_title", "Meeting analysis")
    result.setdefault("summary", "No summary returned.")
    result.setdefault("overall_status", "Review required")
    return result

def ask_meeting(transcript, question, model, base_url):
    prompt = f"""Answer the user's question using ONLY the transcript below.
If the answer is absent, say: "The transcript does not specify this."
Include a short supporting quote where possible. Be concise.
Transcript:
{transcript[:30000]}
Question: {question}
Answer:"""
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=180,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()

def render_list(items, empty_text):
    if not items:
        st.info(empty_text)
    else:
        for item in items:
            st.markdown(f'<div class="decision">{item}</div>', unsafe_allow_html=True)

def make_download(report):
    return json.dumps(report, indent=2, ensure_ascii=False).encode("utf-8")

# ----------------------------- Sidebar ---------------------------------
with st.sidebar:
    st.markdown("## 🧠 MeetingMind")
    st.caption("Meeting intelligence workspace")
    page = st.radio("WORKSPACE", ["Overview", "Analyze Meeting", "Ask Meeting", "Meeting History", "About Project"], label_visibility="visible")
    st.divider()
    st.markdown("**LOCAL AI SETTINGS**")
    model = st.text_input("Ollama model", value=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"))
    base_url = st.text_input("Ollama URL", value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    st.caption("Start Ollama locally to enable AI analysis.")
    if st.button("Check AI connection", use_container_width=True):
        try:
            r = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=5)
            r.raise_for_status()
            names = [m.get("name") for m in r.json().get("models", [])]
            st.success("Ollama is running")
            st.caption("Installed: " + (", ".join(names) if names else "No models found"))
        except Exception:
            st.error("Cannot connect. Start Ollama and check the URL.")

history = load_history()
if "transcript" not in st.session_state: st.session_state.transcript = ""
if "report" not in st.session_state: st.session_state.report = None
if "active_meeting" not in st.session_state: st.session_state.active_meeting = None

# ----------------------------- Header ----------------------------------
st.markdown("""
<div class="hero">
 <div class="eyebrow">YOUR AI-POWERED MEETING WORKSPACE</div>
 <div class="hero-title">Turn conversations into clear outcomes.</div>
 <div class="hero-sub">Summaries, decisions, owners and next steps — organized in one intelligent workspace.</div>
 <div style="margin-top:13px"><span class="pill">✦ AI Summarization</span><span class="pill">✓ Decision Tracking</span><span class="pill">↗ Action Items</span><span class="pill">⌕ Ask Your Meeting</span></div>
</div>
""", unsafe_allow_html=True)

# ----------------------------- Overview --------------------------------
if page == "Overview":
    c1,c2,c3,c4 = st.columns(4)
    total = len(history)
    total_actions = sum(len(x.get("report",{}).get("action_items",[])) for x in history)
    total_decisions = sum(len(x.get("report",{}).get("decisions",[])) for x in history)
    c1.metric("Meetings analyzed", total)
    c2.metric("Action items tracked", total_actions)
    c3.metric("Decisions captured", total_decisions)
    c4.metric("AI workspace", "Ready" if st.session_state.report else "Idle")
    left,right = st.columns([1.35,1])
    with left:
        st.markdown('<div class="panel"><div class="section-title">Welcome to MeetingMind AI</div><p class="small-muted">Stop replaying long recordings and searching through scattered notes. Upload a transcript to create a structured, searchable meeting report.</p></div>', unsafe_allow_html=True)
        st.markdown("#### Quick start")
        st.markdown("1. Open **Analyze Meeting**.")
        st.markdown("2. Paste a transcript or upload a `.txt` file.")
        st.markdown("3. Generate the summary, decisions and action items.")
        st.markdown("4. Ask questions or revisit reports in Meeting History.")
        if st.button("＋ Analyze a meeting", use_container_width=True):
            st.session_state["jump_analyze"] = True
            st.rerun()
    with right:
        st.markdown('<div class="panel"><div class="section-title">Processing pipeline</div><p>① Transcript input</p><p>↓</p><p>② Topic & context understanding</p><p>↓</p><p>③ Decision and task extraction</p><p>↓</p><p>④ Evidence verification</p><p>↓</p><p>⑤ Meeting intelligence report</p></div>', unsafe_allow_html=True)
    if history:
        st.markdown("#### Recent meetings")
        for item in history[:3]:
            st.markdown(f'<div class="task"><b>{item.get("title","Untitled meeting")}</b><br><span class="small-muted">{item.get("created_at","")}</span></div>', unsafe_allow_html=True)

# ----------------------------- Analyze ----------------------------------
elif page == "Analyze Meeting":
    st.markdown("### Analyze a meeting")
    st.caption("Paste a transcript or upload a plain-text transcript. Keep the original transcript for verification.")
    uploaded = st.file_uploader("Upload transcript (.txt)", type=["txt"])
    if uploaded:
        try:
            st.session_state.transcript = uploaded.read().decode("utf-8", errors="replace")
        except Exception as e:
            st.error(f"Could not read file: {e}")
    meeting_title = st.text_input("Meeting title", value="Project planning meeting")
    transcript = st.text_area("Meeting transcript", key="transcript", height=280, placeholder="Paste speaker-labelled meeting transcript here...")
    col_a,col_b = st.columns([1,2])
    with col_a:
        run_analysis = st.button("✦ Generate meeting report", use_container_width=True)
    with col_b:
        st.caption("AI mode requires Ollama + the selected model. If unavailable, a clearly labelled offline demo fallback is used.")
    if run_analysis:
        if len(transcript.strip()) < 30:
            st.warning("Please provide a longer transcript (at least 30 characters).")
        else:
            with st.spinner("Reading transcript and extracting meeting intelligence..."):
                try:
                    report = analyze_meeting(transcript, model, base_url)
                    report["analysis_mode"] = "Ollama / " + model
                except Exception as e:
                    report = fallback_analysis(transcript)
                    report["analysis_mode"] = "Offline demo fallback"
                    report["verification_notes"].append(f"AI connection detail: {str(e)[:180]}")
                report["meeting_title"] = meeting_title.strip() or report.get("meeting_title","Meeting analysis")
                st.session_state.report = report
                st.session_state.active_meeting = {"title": report["meeting_title"], "transcript": transcript, "report": report}
                item = {"title": report["meeting_title"], "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"), "transcript": transcript, "report": report}
                history.insert(0, item)
                save_history(history)
            st.success("Meeting report generated.")
    report = st.session_state.report
    if report:
        st.divider()
        st.markdown(f"## {report.get('meeting_title','Meeting report')}")
        st.markdown(f'<span class="pill">Mode: {report.get("analysis_mode","AI")}</span><span class="pill">Status: {report.get("overall_status","Review required")}</span>', unsafe_allow_html=True)
        if report.get("analysis_mode") == "Offline demo fallback":
            st.warning("Offline demo mode: this is a basic rule-based preview, not a Qwen-generated report. Start Ollama for full AI extraction.")
        st.markdown("### 📝 Meeting summary")
        st.markdown(f'<div class="panel">{report.get("summary","")}</div>', unsafe_allow_html=True)
        tab1,tab2,tab3,tab4 = st.tabs(["Key decisions", "Action items", "Open questions", "Verification"])
        with tab1:
            if report.get("decisions"):
                for d in report["decisions"]:
                    if isinstance(d, dict):
                        st.markdown(f'<div class="decision"><b>{d.get("decision","")}</b><br><span class="small-muted">Reason: {d.get("reason","Not specified")} · Participants: {d.get("participants","Not specified")}</span><br><span class="small-muted">Evidence: {d.get("evidence","Not provided")}</span></div>', unsafe_allow_html=True)
                    else: st.markdown(f"- {d}")
            else: st.info("No explicit decisions were extracted.")
        with tab2:
            tasks = report.get("action_items", [])
            if tasks:
                for i,t in enumerate(tasks,1):
                    if isinstance(t,dict):
                        st.markdown(f'<div class="task"><b>{i}. {t.get("task","")}</b><br><span class="small-muted">Owner: {t.get("owner","Not specified")} &nbsp; | &nbsp; Deadline: {t.get("deadline","Not specified")} &nbsp; | &nbsp; Status: {t.get("status","Open")}</span><br><span class="small-muted">Evidence: {t.get("evidence","Not provided")}</span></div>', unsafe_allow_html=True)
                    else: st.markdown(f"- {t}")
            else: st.info("No action items were extracted.")
        with tab3:
            render_list(report.get("open_questions", []), "No open questions were identified.")
        with tab4:
            st.markdown("**Key points**")
            render_list(report.get("key_points", []), "No key points.")
            st.markdown("**Verification notes**")
            render_list(report.get("verification_notes", []), "No verification notes.")
        st.download_button("⬇ Download report (JSON)", data=make_download(report), file_name="meetingmind_report.json", mime="application/json")

# ----------------------------- Ask Meeting ------------------------------
elif page == "Ask Meeting":
    st.markdown("### Ask your meeting")
    st.caption("Ask questions grounded in the transcript. The assistant should say when information is not available.")
    if st.session_state.active_meeting:
        transcript_for_qa = st.session_state.active_meeting["transcript"]
        st.info("Active meeting: " + st.session_state.active_meeting["title"])
    elif history:
        choices = [x.get("title","Untitled") for x in history]
        selected = st.selectbox("Choose a saved meeting", choices)
        selected_item = next(x for x in history if x.get("title") == selected)
        transcript_for_qa = selected_item.get("transcript","")
    else:
        transcript_for_qa = ""
        st.warning("Analyze a meeting first, or save a report to Meeting History.")
    question = st.text_input("Your question", placeholder="What decision was made about the project budget?")
    if st.button("Ask Meeting AI"):
        if not transcript_for_qa:
            st.warning("No transcript is available.")
        elif not question.strip():
            st.warning("Enter a question.")
        else:
            try:
                with st.spinner("Searching the transcript..."):
                    answer = ask_meeting(transcript_for_qa, question, model, base_url)
                st.markdown("#### Answer")
                st.markdown(f'<div class="panel">{answer}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Ask Meeting requires a running Ollama model. " + str(e)[:220])

# ----------------------------- History ----------------------------------
elif page == "Meeting History":
    st.markdown("### Meeting history")
    st.caption("Reports are stored locally in the project's data folder. MongoDB integration can be enabled in a later deployment.")
    if not history:
        st.info("No meetings saved yet. Analyze your first transcript.")
    else:
        search = st.text_input("Search meetings", placeholder="Search by meeting title")
        filtered = [x for x in history if search.lower() in x.get("title","").lower()]
        for idx,item in enumerate(filtered):
            with st.expander(f"{item.get('title','Untitled')}  ·  {item.get('created_at','')}"):
                st.write(item.get("report",{}).get("summary","No summary"))
                st.caption(f"{len(item.get('report',{}).get('action_items',[]))} action items · {len(item.get('report',{}).get('decisions',[]))} decisions")
                if st.button("Load this report", key=f"load_{idx}"):
                    st.session_state.report = item.get("report")
                    st.session_state.active_meeting = item
                    st.success("Loaded. Open Analyze Meeting to view the full report.")
        if st.button("Clear local meeting history"):
            save_history([])
            st.warning("History cleared. Refresh the page.")

# ----------------------------- About ------------------------------------
elif page == "About Project":
    st.markdown("### About MeetingMind AI")
    st.markdown("""
<div class="panel">
<b>Problem statement</b><br>
Important meeting outcomes are often lost in long transcripts. MeetingMind AI converts conversations into structured, searchable meeting intelligence.<br><br>
<b>Core modules</b><br>
• Transcript preprocessing and chunk-ready input<br>
• Query-focused meeting question answering<br>
• Summary and key-point generation<br>
• Decision and action-item extraction<br>
• Evidence-based verification notes<br>
• Meeting history and report export
</div>
""", unsafe_allow_html=True)
    st.markdown("#### Agentic workflow")
    st.code("Transcript → Topic Detection → Decision Extraction → Action-Item Extraction → Consistency Checker → Final Report", language="text")
    st.markdown("#### Dataset and evaluation")
    st.write("Use QMSum for query-focused meeting summarization experiments. Evaluate generated summaries with ROUGE and manually assess decision/action-item correctness and factual consistency.")
    st.markdown("#### Limitations")
    st.write("This student prototype is a decision-support tool. Human review is required before assigning tasks or treating extracted decisions as official records.")
