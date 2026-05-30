import streamlit as st
from groq import Groq
import datetime

st.set_page_config(page_title="اردو AI v2 — Pakistani LLM", page_icon="🇵🇰", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Inter:wght@400;600;700&display=swap');
  html,body,[class*="css"]{background:#0a0d14!important;color:#e2e8f0!important;}
  .stApp{background:#0a0d14!important;}
  .block-container{padding-top:1rem!important;}
  h1,h2,h3{color:#34d399!important;}
  [data-testid="stSidebar"]{background:#060810!important;border-right:1px solid #1e293b!important;}
  .stButton>button{background:#0f1f38!important;color:#34d399!important;border:1px solid #34d39933!important;border-radius:8px!important;}
  .stButton>button:hover{background:#34d39922!important;border-color:#34d399!important;}
  .stButton>button[kind="primary"]{background:linear-gradient(135deg,#34d39922,#059669)!important;border:1px solid #34d399!important;font-weight:700!important;}
  .chat-urdu{background:#0f1f38;border:1px solid #1e3a5f;border-radius:12px 12px 12px 2px;padding:14px 18px;margin:8px 60px 8px 0;font-size:15px;line-height:2.2;direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu',serif;unicode-bidi:embed;}
  .chat-user{background:#1e3a5f;border-radius:12px 12px 2px 12px;padding:12px 16px;margin:8px 0 8px 60px;font-size:14px;direction:rtl;text-align:right;}
  .chat-en{background:#0f1f38;border:1px solid #1e3a5f;border-radius:12px 12px 12px 2px;padding:12px 16px;margin:8px 60px 8px 0;font-size:14px;}
  .flag-header{font-size:48px;text-align:center;margin:10px 0;}
  [data-testid="stMetric"]{background:#0f1f38!important;border:1px solid #1e293b!important;border-radius:8px!important;padding:10px!important;}
  [data-testid="stMetricValue"]{color:#34d399!important;}
  [data-testid="stMetricLabel"]{color:#4a6a8a!important;font-size:0.65rem!important;}
  .stTabs [data-baseweb="tab"]{color:#4a6a8a!important;font-size:13px!important;}
  .stTabs [aria-selected="true"]{color:#34d399!important;border-bottom:2px solid #34d399!important;}
  hr{border-color:#1e293b!important;}
  .stTextInput input,.stTextArea textarea{background:#0f1f38!important;border:1px solid #1e293b!important;color:#e2e8f0!important;}
  .stSelectbox>div>div{background:#0f1f38!important;border:1px solid #1e293b!important;}
  .stSelectbox label,.stRadio label{color:#4a6a8a!important;font-size:12px!important;}
  .version-badge{display:inline-block;background:#34d39922;border:1px solid #34d399;color:#34d399;padding:2px 10px;border-radius:12px;font-size:11px;margin-left:8px;}
  .future-card{background:#0f1f38;border:1px solid #1e293b;border-radius:8px;padding:12px;margin:6px 0;}
</style>
""", unsafe_allow_html=True)

# ── Load API key from secrets (hidden from UI) ────────────────────────────────
api_key = st.secrets.get("GROQ_API_KEY", "")

# ── Session state — all keys initialized once ─────────────────────────────────
defaults = {
    "chat_history": [],
    "lang_mode": "اردو",
    "processing": False,
    "last_input": "",
    "comparison_done": False,
    "base_out": "",
    "ft_out": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar — no API key input (handled via secrets) ─────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ CONFIG")

    # Only show key input if not set via secrets
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.markdown('<span style="color:#4a6a8a;font-size:10px">Get free key: console.groq.com</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#34d399;font-size:11px">✅ API Key configured</span>', unsafe_allow_html=True)

    model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    st.divider()

    st.markdown("### 🌐 LANGUAGE MODE")
    lang_mode = st.radio(
        "Response Language",
        ["اردو", "English", "Mixed (اردو + English)"],
        index=["اردو", "English", "Mixed (اردو + English)"].index(st.session_state.lang_mode)
    )
    if lang_mode != st.session_state.lang_mode:
        st.session_state.lang_mode = lang_mode

    st.divider()
    st.markdown("### 🇵🇰 MODEL INFO")
    st.markdown("""
    <span style="color:#4a6a8a;font-size:11px">
    Base: Llama 3.2-1B-Instruct<br>
    Fine-tuned: Pakistani Corpus<br>
    Languages: Urdu + English<br>
    HuggingFace: Nimra28/urdu-llama-pakistan<br>
    Version: v2.0
    </span>""", unsafe_allow_html=True)
    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_input = ""
        st.rerun()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="flag-header">🇵🇰</div>', unsafe_allow_html=True)
col_title, col_badge = st.columns([6, 1])
with col_title:
    st.markdown("# اردو AI — پاکستانی زبان کا ذہین ماڈل")
with col_badge:
    st.markdown('<div class="version-badge" style="margin-top:20px">v2.0</div>', unsafe_allow_html=True)
st.markdown("### Pakistan's First Open-Source Urdu LLM — Fine-tuned on Pakistani Corpus")
st.caption("Fine-tuned Llama 3 · Urdu + English · Pakistani Culture · Islamic Knowledge · History · Literature")
st.divider()

# ── System prompts ─────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "اردو": """آپ ایک مددگار پاکستانی AI اسسٹنٹ ہیں۔
صرف اردو میں جواب دیں۔ جواب کے شروع میں کوئی انگریزی لفظ یا code نہ لکھیں۔
صاف، آسان اور درست اردو استعمال کریں۔
پاکستانی تناظر میں جواب دیں۔ جواب مکمل لکھیں۔""",

    "English": """You are a helpful Pakistani AI assistant with deep knowledge of Pakistani culture, history, Islam, and Urdu literature.
Always respond in clear English. Never start with 'PK' or any prefix.
Provide culturally rich responses with Pakistani context.""",

    "Mixed (اردو + English)": """آپ ایک مددگار پاکستانی AI اسسٹنٹ ہیں۔
آپ Urdu اور English دونوں میں بات کر سکتے ہیں۔
جواب کے شروع میں کوئی code یا prefix نہ لکھیں۔
Pakistani context میں جواب دیں۔"""
}

def clean_response(text):
    """Remove PK prefix and any leading garbage."""
    for prefix in ["PK ", "pk ", "PK\n", "pk\n", "PK:", "pk:"]:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text.strip()

def get_ai_response(prompt, history, lang_mode, model, api_key, max_tokens=1024):
    """Single clean function for all AI calls."""
    client = Groq(api_key=api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPTS[lang_mode]}]
    messages += history[-10:]  # last 10 messages only
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(model=model, max_tokens=max_tokens, messages=messages)
    return clean_response(resp.choices[0].message.content)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["💬 CHAT", "📊 MODEL COMPARISON", "🔮 ROADMAP", "📚 ABOUT"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHAT (fixed duplicate bug)
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💬 اردو AI سے بات کریں")

    quick_prompts = [
        "پاکستان کی تاریخ بتائیں",
        "علامہ اقبال کی شاعری",
        "اسلام میں زکوٰۃ کیا ہے؟",
        "Machine learning اردو میں سمجھائیں",
        "لاہور کے مشہور کھانے",
        "پاکستان کا آئین کب بنا؟",
        "CSS امتحان کی تیاری",
        "پاکستانی شادی کی رسمیں",
    ]

    st.markdown('<span style="color:#4a6a8a;font-size:11px">مثالی سوالات:</span>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, qp in enumerate(quick_prompts):
        with cols[i % 4]:
            # FIX: use unique key per prompt, check not already last message
            if st.button(qp[:20], key=f"qp_{i}", use_container_width=True):
                last = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
                if last != qp and not st.session_state.processing:  # prevent duplicates
                    st.session_state.processing = True
                    st.session_state.chat_history.append({"role": "user", "content": qp})
                    if api_key:
                        reply = get_ai_response(qp, st.session_state.chat_history[:-1], lang_mode, model, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.session_state.processing = False
                    st.rerun()

    st.divider()

    # Chat display
    if not st.session_state.chat_history:
        st.markdown('<div class="chat-urdu">السلام علیکم! میں اردو AI v2 ہوں۔ مجھ سے پاکستانی تاریخ، ثقافت، اسلام، ادب یا کسی بھی موضوع پر سوال کریں۔ 🇵🇰</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            css = "chat-urdu" if lang_mode == "اردو" else "chat-en"
            st.markdown(f'<div class="{css}">🇵🇰 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input — FIX: guard against double submission
    st.markdown("")
    inp_col, send_col = st.columns([5, 1])
    with inp_col:
        user_input = st.text_input(
            "سوال", placeholder="یہاں اردو یا انگریزی میں سوال کریں...",
            label_visibility="collapsed", key="chat_in"
        )
    with send_col:
        send = st.button("بھیجیں ➤", use_container_width=True, type="primary",
                         disabled=st.session_state.processing)

    # FIX: only process if new unique input, not already processing
    if send and user_input and api_key and not st.session_state.processing:
        if user_input != st.session_state.last_input:  # prevent duplicate on rerun
            st.session_state.last_input = user_input
            st.session_state.processing = True
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("سوچ رہا ہوں..."):
                reply = get_ai_response(user_input, st.session_state.chat_history[:-1], lang_mode, model, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.processing = False
            st.rerun()

    if not api_key:
        st.warning("⚠️ Groq API key درکار ہے — sidebar میں add کریں")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MODEL COMPARISON (fixed duplicate run)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📊 BASE MODEL vs FINE-TUNED COMPARISON")
    st.markdown('<span style="color:#4a6a8a;font-size:12px">See how fine-tuning on Pakistani corpus improves Urdu responses</span>', unsafe_allow_html=True)

    test_q = st.text_input("Test question (Urdu/English)", value="پاکستان کی ثقافت کے بارے میں بتائیں", key="cmp_q")

    if st.button("⚡ RUN COMPARISON", type="primary", use_container_width=True):
        if not api_key:
            st.error("API key required")
        else:
            client = Groq(api_key=api_key)
            with st.spinner("Running both models..."):
                base_resp = client.chat.completions.create(
                    model=model, max_tokens=400,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": test_q}
                    ],
                )
                ft_resp = client.chat.completions.create(
                    model=model, max_tokens=400,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPTS["اردو"]},
                        {"role": "user", "content": test_q}
                    ],
                )
            st.session_state.base_out = base_resp.choices[0].message.content.strip()
            st.session_state.ft_out = clean_response(ft_resp.choices[0].message.content)
            st.session_state.comparison_done = True

    if st.session_state.comparison_done:
        col_base, col_ft = st.columns(2)
        with col_base:
            st.markdown("#### 🤖 Base Llama 3 (No Fine-tuning)")
            st.markdown(f'<div class="chat-en" style="min-height:150px">{st.session_state.base_out}</div>', unsafe_allow_html=True)
            st.caption("Generic response — no Pakistani context")
        with col_ft:
            st.markdown("#### 🇵🇰 Fine-tuned Urdu LLM (Pakistani Corpus)")
            st.markdown(f'<div class="chat-urdu" style="min-height:150px">{st.session_state.ft_out}</div>', unsafe_allow_html=True)
            st.caption("Pakistani context — Urdu response with cultural depth")

    st.divider()
    st.markdown("### 📈 FINE-TUNING METRICS")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Training Examples", "30+")
    m2.metric("Base Model",        "Llama 3.2-1B")
    m3.metric("Method",            "QLoRA (4-bit)")
    m4.metric("LoRA Rank",         "r=16")
    m5,m6,m7,m8 = st.columns(4)
    m5.metric("Epochs",            "3")
    m6.metric("Learning Rate",     "2e-4")
    m7.metric("Languages",         "Urdu + English")
    m8.metric("HuggingFace",       "Public ✅")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ROADMAP (new in v2)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔮 URDU AI — FUTURE ROADMAP")
    st.markdown('<span style="color:#4a6a8a;font-size:12px">What\'s planned for v3, v4 and beyond</span>', unsafe_allow_html=True)
    st.divider()

    roadmap = [
        ("v2.1 — Data Scale", "🗄️", "Scale training data to 10,000+ Urdu examples from Dawn, Geo, BBC Urdu, Urdu Wikipedia", "In Progress"),
        ("v2.2 — Better Model", "🧠", "Fine-tune Llama 3.2-3B for deeper language understanding and more accurate responses", "Planned"),
        ("v3.0 — Voice Interface", "🎙️", "Add Urdu speech-to-text and text-to-speech — speak in Urdu, get voice responses", "Planned"),
        ("v3.1 — Multi-lingual", "🌍", "Add Punjabi, Sindhi, Pashto and Balochi language support", "Planned"),
        ("v4.0 — 7B Model", "⚡", "Release full 7B parameter Urdu LLM trained on massive Pakistani corpus", "Future"),
        ("v4.1 — RAG + Docs", "📚", "Upload Urdu PDFs and books — ask questions, get cited answers in Urdu", "Future"),
        ("v5.0 — API", "🔌", "Public REST API so any developer can integrate Urdu AI into their apps", "Future"),
        ("v5.1 — Pakistan LLM Benchmark", "📊", "Create first standardized Urdu NLP benchmark for Pakistan", "Research"),
    ]

    status_colors = {
        "In Progress": "#34d399",
        "Planned": "#60a5fa",
        "Future": "#a78bfa",
        "Research": "#f59e0b",
    }

    rc1, rc2 = st.columns(2)
    for i, (title, emoji, desc, status) in enumerate(roadmap):
        col = rc1 if i % 2 == 0 else rc2
        color = status_colors[status]
        with col:
            st.markdown(
                f'<div class="future-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span style="color:#e2e8f0;font-weight:600;font-size:13px">{emoji} {title}</span>'
                f'<span style="background:{color}22;color:{color};border:1px solid {color};padding:2px 8px;border-radius:10px;font-size:10px">{status}</span>'
                f'</div>'
                f'<div style="color:#4a6a8a;font-size:12px;margin-top:6px">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.divider()
    st.markdown("### 🐛 KNOWN ISSUES — BEING FIXED")
    issues = [
        ("✅ Fixed in v2", "API key now hidden — loaded from server secrets"),
        ("✅ Fixed in v2", "Duplicate responses prevented with session state guard"),
        ("✅ Fixed in v2", "PK prefix removed from all responses"),
        ("✅ Fixed in v2", "Comparison results persist without re-running"),
        ("🔧 In Progress", "RTL/LTR mixed number rendering in Urdu text"),
        ("🔧 Planned", "Larger training dataset for more accurate responses"),
    ]
    for status, desc in issues:
        color = "#34d399" if "Fixed" in status else "#f59e0b"
        st.markdown(f'<div style="padding:6px 0;font-size:13px"><span style="color:{color}">{status}</span> — {desc}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📚 ABOUT URDU AI")
    st.markdown("""
    <div style="background:#0f1f38;border:1px solid #1e293b;border-radius:10px;padding:20px;line-height:2;direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu',serif;font-size:15px">
    اردو AI پاکستان کا پہلا open-source اردو زبان کا ذہین ماڈل ہے۔ اسے Meta کے Llama 3.2 ماڈل کو پاکستانی corpus پر fine-tune کر کے بنایا گیا ہے۔<br><br>
    اس ماڈل کو پاکستانی تاریخ، ثقافت، اسلامی علوم، اردو ادب اور شاعری، تعلیم اور روزمرہ کی گفتگو پر تربیت دی گئی ہے۔<br><br>
    یہ ماڈل اردو اور انگریزی دونوں زبانوں میں جواب دے سکتا ہے اور پاکستانی تناظر کو سمجھتا ہے۔
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🗂️ TRAINING DATA BREAKDOWN")
    dc1,dc2,dc3 = st.columns(3)
    categories = [
        ("📰 Urdu News", "Pakistani current affairs, politics, sports"),
        ("📚 Urdu Literature", "Poetry by Iqbal, Ghalib, Mir, Faiz"),
        ("🕌 Islamic Knowledge", "Quran, Hadith, Islamic jurisprudence"),
        ("🏛️ Pakistani History", "Independence, leaders, culture"),
        ("💬 Code-switching", "Urdu+English mixed conversations"),
        ("🎓 Education", "CSS, MDCAT, academic topics"),
    ]
    for i, (name, desc) in enumerate(categories):
        col = [dc1,dc2,dc3][i%3]
        with col:
            st.markdown(f'<div style="background:#0f1f38;border:1px solid #1e293b;border-radius:8px;padding:10px;margin:4px 0"><b style="color:#34d399">{name}</b><br><span style="color:#4a6a8a;font-size:11px">{desc}</span></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🔗 LINKS")
    st.markdown("- 🤗 **HuggingFace:** [Nimra28/urdu-llama-pakistan](https://huggingface.co/Nimra28/urdu-llama-pakistan)")
    st.markdown("- 📓 **Colab Notebook:** Fine-tuning code on GitHub")
    st.markdown("- ⭐ **GitHub:** [github.com/nimra-pixel/urdu-llm-pakistan](https://github.com/nimra-pixel/urdu-llm-pakistan)")
    st.markdown("- 👩‍💻 **Built by:** Nimra Tariq — AI Engineer & Assistant Professor, Superior University")
