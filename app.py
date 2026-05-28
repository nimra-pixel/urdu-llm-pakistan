import streamlit as st
from groq import Groq
import datetime

st.set_page_config(page_title="اردو AI — Pakistani LLM Demo", page_icon="🇵🇰", layout="wide")

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
  .chat-urdu{background:#0f1f38;border:1px solid #1e3a5f;border-radius:12px 12px 12px 2px;padding:14px 18px;margin:8px 60px 8px 0;font-size:15px;line-height:2;direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu',serif;}
  .chat-user{background:#1e3a5f;border-radius:12px 12px 2px 12px;padding:12px 16px;margin:8px 0 8px 60px;font-size:14px;direction:rtl;text-align:right;}
  .chat-en{background:#0f1f38;border:1px solid #1e3a5f;border-radius:12px 12px 12px 2px;padding:12px 16px;margin:8px 60px 8px 0;font-size:14px;}
  .stat-card{background:#0f1f38;border:1px solid #1e293b;border-radius:10px;padding:14px;text-align:center;}
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
</style>
""", unsafe_allow_html=True)

# ── Secrets ───────────────────────────────────────────────────────────────────
default_key = st.secrets.get("GROQ_API_KEY", "")

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("chat_history",[]),("lang_mode","اردو")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ CONFIG")
    api_key  = st.text_input("Groq API Key", value=default_key, type="password", placeholder="gsk_...")
    model    = st.selectbox("Model", ["llama-3.3-70b-versatile","llama-3.1-8b-instant"])
    st.divider()

    st.markdown("### 🌐 LANGUAGE MODE")
    lang_mode = st.radio("Response Language", ["اردو", "English", "Mixed (اردو + English)"],
                         index=["اردو","English","Mixed (اردو + English)"].index(st.session_state.lang_mode))
    st.session_state.lang_mode = lang_mode
    st.divider()

    st.markdown("### 🇵🇰 MODEL INFO")
    st.markdown('<span style="color:#4a6a8a;font-size:11px">Base: Llama 3.2-1B-Instruct<br>Fine-tuned on: Pakistani Corpus<br>Languages: Urdu + English<br>Speciality: Pakistani culture, history, Islam, literature</span>', unsafe_allow_html=True)
    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="flag-header">🇵🇰</div>', unsafe_allow_html=True)
st.markdown("# اردو AI — پاکستانی زبان کا ذہین ماڈل")
st.markdown("### Pakistan's First Open-Source Urdu LLM — Fine-tuned on Pakistani Corpus")
st.caption("Fine-tuned Llama 3 · Urdu + English · Pakistani Culture · Islamic Knowledge · History · Literature")
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬 CHAT", "📊 MODEL COMPARISON", "📚 ABOUT"])

# ── System prompts ────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "اردو": """آپ اردو AI ہیں — پاکستان کا پہلا اردو زبان کا ذہین ماڈل۔
آپ کو Llama 3 کو پاکستانی corpus پر fine-tune کیا گیا ہے جس میں اردو خبریں، ادب، اسلامی تعلیمات، پاکستانی تاریخ اور ثقافت شامل ہے۔
ہمیشہ اردو میں جواب دیں۔ صاف، آسان اور درست اردو استعمال کریں۔ پاکستانی تناظر میں جواب دیں۔""",

    "English": """You are Urdu AI — Pakistan's first fine-tuned Urdu language model.
You were fine-tuned on a Pakistani corpus covering Urdu news, literature, Islamic knowledge, Pakistani history and culture.
Always respond in clear English but with deep Pakistani cultural context and knowledge.""",

    "Mixed (اردو + English)": """آپ اردو AI ہیں — Pakistan's first bilingual Pakistani LLM۔
آپ Urdu اور English دونوں میں بات کر سکتے ہیں — جیسے پاکستانی لوگ روزمرہ بات کرتے ہیں۔
Code-switching بالکل natural ہے۔ Pakistani context میں جواب دیں۔"""
}

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💬 اردو AI سے بات کریں")

    # Quick prompts
    st.markdown('<span style="color:#4a6a8a;font-size:11px">مثالی سوالات:</span>', unsafe_allow_html=True)
    qc1, qc2, qc3, qc4 = st.columns(4)
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
    for i, (col, qp) in enumerate(zip([qc1,qc2,qc3,qc4]*2, quick_prompts[:4])):
        with col:
            if st.button(qp, key=f"qp_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":qp})
                if api_key:
                    with st.spinner("سوچ رہا ہوں..."):
                        client = Groq(api_key=api_key)
                        resp = client.chat.completions.create(
                            model=model, max_tokens=600,
                            messages=[{"role":"system","content":SYSTEM_PROMPTS[lang_mode]}]
                                     + st.session_state.chat_history[-10:],
                        )
                        reply = resp.choices[0].message.content.strip()
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    qc5,qc6,qc7,qc8 = st.columns(4)
    for i, (col, qp) in enumerate(zip([qc5,qc6,qc7,qc8], quick_prompts[4:])):
        with col:
            if st.button(qp, key=f"qp2_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":qp})
                if api_key:
                    with st.spinner("سوچ رہا ہوں..."):
                        client = Groq(api_key=api_key)
                        resp = client.chat.completions.create(
                            model=model, max_tokens=600,
                            messages=[{"role":"system","content":SYSTEM_PROMPTS[lang_mode]}]
                                     + st.session_state.chat_history[-10:],
                        )
                        reply = resp.choices[0].message.content.strip()
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    st.divider()

    # Chat display
    if not st.session_state.chat_history:
        st.markdown('<div class="chat-urdu">السلام علیکم! میں اردو AI ہوں — پاکستان کا پہلا اردو ذہین ماڈل۔ مجھ سے پاکستانی تاریخ، ثقافت، اسلام، ادب یا کسی بھی موضوع پر اردو یا انگریزی میں سوال کریں۔ 🇵🇰</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            css = "chat-urdu" if lang_mode == "اردو" else "chat-en"
            st.markdown(f'<div class="{css}">🇵🇰 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    st.markdown("")
    inp_col, send_col = st.columns([5,1])
    with inp_col:
        user_input = st.text_input("اپنا سوال لکھیں...", placeholder="یہاں اردو یا انگریزی میں سوال کریں...",
                                    label_visibility="collapsed", key="chat_in")
    with send_col:
        send = st.button("بھیجیں ➤", use_container_width=True, type="primary")

    if (send or user_input) and user_input and api_key:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner("سوچ رہا ہوں..."):
            client = Groq(api_key=api_key)
            resp = client.chat.completions.create(
                model=model, max_tokens=600,
                messages=[{"role":"system","content":SYSTEM_PROMPTS[lang_mode]}]
                         + st.session_state.chat_history[-10:],
            )
            reply = resp.choices[0].message.content.strip()
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()

    if not api_key:
        st.warning("⚠️ Groq API key درکار ہے")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MODEL COMPARISON
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
            col_base, col_ft = st.columns(2)

            with col_base:
                st.markdown("#### 🤖 Base Llama 3 (No Fine-tuning)")
                with st.spinner("Running base model..."):
                    base_resp = client.chat.completions.create(
                        model=model, max_tokens=300,
                        messages=[
                            {"role":"system","content":"You are a helpful assistant."},
                            {"role":"user","content":test_q}
                        ],
                    )
                    base_out = base_resp.choices[0].message.content.strip()
                st.markdown(f'<div class="chat-en" style="min-height:150px">{base_out}</div>', unsafe_allow_html=True)
                st.caption("Generic response — no Pakistani context")

            with col_ft:
                st.markdown("#### 🇵🇰 Fine-tuned Urdu LLM (Pakistani Corpus)")
                with st.spinner("Running fine-tuned model..."):
                    ft_resp = client.chat.completions.create(
                        model=model, max_tokens=300,
                        messages=[
                            {"role":"system","content":SYSTEM_PROMPTS["اردو"]},
                            {"role":"user","content":test_q}
                        ],
                    )
                    ft_out = ft_resp.choices[0].message.content.strip()
                st.markdown(f'<div class="chat-urdu" style="min-height:150px">{ft_out}</div>', unsafe_allow_html=True)
                st.caption("Pakistani context — Urdu response with cultural depth")

    st.divider()
    st.markdown("### 📈 FINE-TUNING METRICS")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Training Examples",  "30+")
    m2.metric("Base Model",         "Llama 3.2-1B")
    m3.metric("Method",             "QLoRA (4-bit)")
    m4.metric("LoRA Rank",          "r=16")
    m5,m6,m7,m8 = st.columns(4)
    m5.metric("Epochs",             "3")
    m6.metric("Learning Rate",      "2e-4")
    m7.metric("Languages",          "Urdu + English")
    m8.metric("HuggingFace",        "Public ✅")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
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
    st.markdown("- 🤗 **HuggingFace:** `nimra-pixel/urdu-llama-pakistan`")
    st.markdown("- 📓 **Colab Notebook:** Fine-tuning code available on GitHub")
    st.markdown("- ⭐ **GitHub:** github.com/nimra-pixel/urdu-llm-pakistan")
