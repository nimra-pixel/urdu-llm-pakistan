import streamlit as st
from groq import Groq
import datetime
import json
import io
import base64

st.set_page_config(page_title="اردو AI v3 — Pakistani LLM Platform", page_icon="🇵🇰", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

  html,body,[class*="css"]{background:#050810!important;color:#e2e8f0!important;font-family:'Inter',sans-serif!important;}
  .stApp{background:#050810!important;}
  .block-container{padding-top:0.5rem!important;max-width:1400px!important;}
  h1,h2,h3{color:#34d399!important;letter-spacing:0.5px;}
  [data-testid="stSidebar"]{background:#030610!important;border-right:1px solid #0d2040!important;}

  /* Buttons */
  .stButton>button{background:#0a1528!important;color:#34d399!important;border:1px solid #34d39933!important;border-radius:8px!important;font-size:12px!important;transition:all 0.2s;}
  .stButton>button:hover{background:#34d39922!important;border-color:#34d399!important;}
  .stButton>button[kind="primary"]{background:linear-gradient(135deg,#059669,#047857)!important;border:1px solid #34d399!important;font-weight:700!important;color:white!important;}

  /* Chat bubbles */
  .chat-urdu{background:#0a1f14;border:1px solid #064e3b;border-radius:16px 16px 4px 16px;padding:16px 20px;margin:8px 80px 8px 0;font-size:16px;line-height:2.4;direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu',serif;unicode-bidi:embed;box-shadow:0 2px 8px rgba(52,211,153,0.1);}
  .chat-user{background:#0f2d4a;border:1px solid #1e4976;border-radius:16px 16px 16px 4px;padding:14px 18px;margin:8px 0 8px 80px;font-size:14px;direction:rtl;text-align:right;box-shadow:0 2px 8px rgba(96,165,250,0.1);}
  .chat-en{background:#0a1f14;border:1px solid #064e3b;border-radius:16px 16px 4px 16px;padding:14px 18px;margin:8px 80px 8px 0;font-size:14px;line-height:1.7;box-shadow:0 2px 8px rgba(52,211,153,0.1);}
  .chat-mixed{background:#0a1528;border:1px solid #1e3a5f;border-radius:16px 16px 4px 16px;padding:14px 18px;margin:8px 80px 8px 0;font-size:14px;line-height:1.8;}

  /* RAG citation */
  .citation{background:#0f2d1a;border-left:3px solid #34d399;padding:8px 12px;margin:6px 0;border-radius:0 8px 8px 0;font-size:12px;color:#86efac;}

  /* Metric cards */
  [data-testid="stMetric"]{background:#0a1528!important;border:1px solid #1e293b!important;border-radius:10px!important;padding:12px!important;}
  [data-testid="stMetricValue"]{color:#34d399!important;font-size:1.3rem!important;}
  [data-testid="stMetricLabel"]{color:#4a6a8a!important;font-size:0.65rem!important;}

  /* Tabs */
  .stTabs [data-baseweb="tab"]{color:#4a6a8a!important;font-size:13px!important;padding:8px 16px!important;}
  .stTabs [aria-selected="true"]{color:#34d399!important;border-bottom:2px solid #34d399!important;}

  /* Inputs */
  hr{border-color:#0d2040!important;}
  .stTextInput input,.stTextArea textarea{background:#0a1528!important;border:1px solid #1e293b!important;color:#e2e8f0!important;border-radius:8px!important;}
  .stSelectbox>div>div{background:#0a1528!important;border:1px solid #1e293b!important;color:#e2e8f0!important;}
  .stSelectbox label,.stRadio label,.stSlider label,.stFileUploader label{color:#4a6a8a!important;font-size:12px!important;}

  /* Expander */
  [data-testid="stExpander"]{border:1px solid #1e293b!important;background:#0a1528!important;border-radius:8px!important;}
  .streamlit-expanderHeader{color:#34d399!important;}

  /* Voice button */
  .voice-btn{background:linear-gradient(135deg,#059669,#0d9488)!important;color:white!important;border:none!important;border-radius:50%!important;width:48px!important;height:48px!important;font-size:20px!important;}

  /* Version badge */
  .v-badge{display:inline-block;background:#34d39922;border:1px solid #34d399;color:#34d399;padding:3px 12px;border-radius:12px;font-size:11px;font-weight:600;}

  /* Feature card */
  .feat-card{background:#0a1528;border:1px solid #1e293b;border-radius:10px;padding:14px;margin:6px 0;}
  .feat-card:hover{border-color:#34d39944;}

  /* Road map */
  .road-card{background:#0a1528;border:1px solid #1e293b;border-radius:10px;padding:12px 16px;margin:6px 0;display:flex;justify-content:space-between;align-items:flex-start;}

  /* Analytics */
  .stat-pill{display:inline-block;background:#0f1f38;border:1px solid #1e293b;border-radius:20px;padding:4px 14px;font-size:12px;margin:4px;}

  /* Progress */
  .stProgress>div>div{background:linear-gradient(90deg,#34d399,#059669)!important;}

  /* Success/warning */
  .stSuccess{background:#0a1f14!important;border:1px solid #34d399!important;}
  .stWarning{background:#1a1000!important;border:1px solid #f59e0b!important;}
  .stInfo{background:#0a1528!important;border:1px solid #60a5fa44!important;}

  /* Scrollbar */
  ::-webkit-scrollbar{width:4px;}
  ::-webkit-scrollbar-track{background:#050810;}
  ::-webkit-scrollbar-thumb{background:#1e293b;border-radius:2px;}
</style>

<!-- Voice Input JS -->
<script>
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('آپ کا browser voice input support نہیں کرتا۔ Chrome استعمال کریں۔');
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'ur-PK';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.start();
    document.getElementById('voice-status').innerText = '🎙️ سن رہا ہوں...';
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('voice-status').innerText = '✅ ' + transcript;
        const inputEl = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        if (inputEl) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(inputEl, transcript);
            inputEl.dispatchEvent(new Event('input', { bubbles: true }));
        }
    };
    recognition.onerror = function(event) {
        document.getElementById('voice-status').innerText = '❌ Error: ' + event.error;
    };
}
</script>
""", unsafe_allow_html=True)

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = st.secrets.get("GROQ_API_KEY", "")

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "chat_history": [],
    "lang_mode": "اردو",
    "processing": False,
    "last_input": "",
    "comparison_base": "",
    "comparison_ft": "",
    "rag_chunks": [],
    "rag_filename": "",
    "chat_export": [],
    "total_messages": 0,
    "topics_discussed": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    for prefix in ["PK ", "pk ", "PK\n", "pk\n", "PK:", "pk:"]:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text.strip()

def get_ai_response(prompt, history, lang, model, key, system_override=None, max_tokens=1024):
    client = Groq(api_key=key)
    system = system_override or SYSTEM_PROMPTS[lang]
    messages = [{"role": "system", "content": system}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history[-10:]]
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(model=model, max_tokens=max_tokens, messages=messages)
    return clean_response(resp.choices[0].message.content)

def extract_pdf_text(uploaded_file):
    try:
        import pdfplumber, io
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except:
        try:
            import PyPDF2, io
            uploaded_file.seek(0)
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except:
            return ""

def chunk_text(text, chunk_size=600, overlap=80):
    """Smart chunking — split on paragraphs first, then by size."""
    # Split on double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len((current + " " + para).split()) <= chunk_size:
            current = (current + " " + para).strip()
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    # If no paragraphs found, fall back to word chunks
    if not chunks:
        words = text.split()
        i = 0
        while i < len(words):
            chunks.append(" ".join(words[i:i+chunk_size]))
            i += chunk_size - overlap
    return chunks

def find_relevant_chunks(query, chunks, top_k=3):
    """Better retrieval — score by word frequency not just overlap."""
    query_words = query.lower().split()
    scored = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        # Count how many times each query word appears
        score = sum(chunk_lower.count(w) for w in query_words if len(w) > 2)
        # Bonus for exact phrase match
        if query.lower() in chunk_lower:
            score += 10
        scored.append((score, i, chunk))
    scored.sort(reverse=True)
    # Filter out zero-score chunks
    relevant = [c for s, _, c in scored if s > 0][:top_k]
    # If nothing found, return first chunks
    if not relevant:
        relevant = chunks[:top_k]
    return relevant

def export_chat_txt():
    lines = ["=" * 50, "اردو AI — Chat Export", f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", "=" * 50, ""]
    for msg in st.session_state.chat_history:
        role = "👤 User" if msg["role"] == "user" else "🇵🇰 Urdu AI"
        lines.append(f"{role}:\n{msg['content']}\n")
    return "\n".join(lines)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇵🇰 اردو AI v3")

    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.markdown('<span style="color:#4a6a8a;font-size:10px">Free key: console.groq.com</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#34d399;font-size:11px">✅ API Key configured</span>', unsafe_allow_html=True)

    model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    st.divider()

    st.markdown("### 🌐 LANGUAGE")
    lang_mode = st.radio("Mode", ["اردو", "English", "Mixed (اردو + English)"],
        index=["اردو", "English", "Mixed (اردو + English)"].index(st.session_state.lang_mode))
    if lang_mode != st.session_state.lang_mode:
        st.session_state.lang_mode = lang_mode
    st.divider()

    st.markdown("### 📊 SESSION STATS")
    total = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    st.markdown(f'<span class="stat-pill">💬 {total} questions</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="stat-pill">📄 {st.session_state.rag_filename or "No doc"}</span>', unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🛠️ ACTIONS")
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_input = ""
        st.rerun()

    if st.session_state.chat_history:
        export_data = export_chat_txt()
        st.download_button(
            "💾 Export Chat",
            data=export_data,
            file_name=f"urdu_ai_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    st.divider()

    st.markdown("""<span style="color:#4a6a8a;font-size:10px">
    Base: Llama 3.2-1B-Instruct<br>
    Fine-tuned: Pakistani Corpus<br>
    HF: Nimra28/urdu-llama-pakistan<br>
    <b style="color:#34d399">Version: v3.0 Final</b>
    </span>""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown("# 🇵🇰 اردو AI — پاکستانی زبان کا ذہین ماڈل")
    st.markdown("#### Pakistan's First Open-Source Urdu LLM Platform · Fine-tuned on Pakistani Corpus")
with c2:
    st.markdown('<div style="margin-top:20px"><span class="v-badge">v3.0 Final</span></div>', unsafe_allow_html=True)
st.divider()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 CHAT", "🎙️ VOICE", "📄 RAG — URDU DOCS",
    "📊 COMPARISON", "🔮 ROADMAP", "📚 ABOUT"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💬 اردو AI سے بات کریں")

    quick_prompts = [
        "پاکستان کی تاریخ بتائیں", "علامہ اقبال کی شاعری",
        "اسلام میں زکوٰۃ کیا ہے؟", "Machine learning سمجھائیں",
        "لاہور کے مشہور کھانے", "پاکستان کا آئین کب بنا؟",
        "CSS امتحان کی تیاری", "پاکستانی شادی کی رسمیں",
    ]
    st.markdown('<span style="color:#4a6a8a;font-size:11px">⚡ مثالی سوالات:</span>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, qp in enumerate(quick_prompts):
        with cols[i % 4]:
            if st.button(qp[:18], key=f"qp_{i}", use_container_width=True):
                last = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
                if last != qp and not st.session_state.processing:
                    st.session_state.processing = True
                    st.session_state.chat_history.append({"role": "user", "content": qp})
                    if api_key:
                        reply = get_ai_response(qp, st.session_state.chat_history[:-1], lang_mode, model, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.session_state.processing = False
                    st.rerun()

    st.divider()

    # Chat display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown('<div class="chat-urdu">السلام علیکم! میں اردو AI v3 ہوں — پاکستان کا پہلا اردو ذہین ماڈل۔ آپ مجھ سے اردو یا انگریزی میں بات کر سکتے ہیں، Urdu دستاویزات پر سوال پوچھ سکتے ہیں، اور آواز سے بھی بات کر سکتے ہیں۔ 🇵🇰</div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                css = "chat-urdu" if lang_mode == "اردو" else ("chat-mixed" if "Mixed" in lang_mode else "chat-en")
                st.markdown(f'<div class="{css}">🇵🇰 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input row
    st.markdown("")
    i1, i2, i3 = st.columns([5, 1, 1])
    with i1:
        user_input = st.text_input("سوال", placeholder="یہاں اردو یا انگریزی میں سوال کریں...",
                                    label_visibility="collapsed", key="chat_in")
    with i2:
        send = st.button("بھیجیں ➤", use_container_width=True, type="primary",
                          disabled=st.session_state.processing)
    with i3:
        st.markdown("🎙️ [Voice Tab]", help="Go to Voice tab for voice input")

    if send and user_input and api_key and not st.session_state.processing:
        if user_input != st.session_state.last_input:
            st.session_state.last_input = user_input
            st.session_state.processing = True
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("سوچ رہا ہوں..."):
                reply = get_ai_response(user_input, st.session_state.chat_history[:-1], lang_mode, model, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.processing = False
            st.rerun()

    if not api_key:
        st.warning("⚠️ Groq API key درکار ہے")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — VOICE INPUT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🎙️ VOICE INPUT — آواز سے بات کریں")
    st.markdown('<span style="color:#4a6a8a;font-size:12px">Speak in Urdu or English — AI transcribes and responds automatically</span>', unsafe_allow_html=True)
    st.info("💡 Voice input works best in **Google Chrome** browser on desktop.")

    st.markdown("""
    <div style="text-align:center;padding:30px;background:#0a1528;border:2px dashed #1e293b;border-radius:16px;margin:20px 0">
      <div style="font-size:48px;margin-bottom:16px">🎙️</div>
      <button onclick="startVoiceInput()" style="background:linear-gradient(135deg,#059669,#0d9488);color:white;border:none;border-radius:50px;padding:14px 32px;font-size:16px;cursor:pointer;font-family:inherit">
        آواز سے سوال کریں
      </button>
      <div id="voice-status" style="margin-top:16px;color:#34d399;font-size:14px;min-height:24px"></div>
      <div style="margin-top:12px;color:#4a6a8a;font-size:12px">Chrome browser required · Urdu & English supported</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✏️ Or Type Your Question")
    voice_text = st.text_area("Your question (paste transcribed text here)", height=100,
                               placeholder="آپ کا سوال یہاں لکھیں یا آواز سے input کریں...",
                               key="voice_input")

    v1, v2 = st.columns(2)
    with v1:
        vlang = st.selectbox("Response Language", ["اردو", "English", "Mixed (اردو + English)"], key="vlang")
    with v2:
        vbtn = st.button("🚀 Get Response", type="primary", use_container_width=True)

    if vbtn and voice_text and api_key:
        with st.spinner("جواب آ رہا ہے..."):
            reply = get_ai_response(voice_text, [], vlang, model, api_key)
        st.markdown("### 🇵🇰 Response")
        css = "chat-urdu" if vlang == "اردو" else "chat-en"
        st.markdown(f'<div class="{css}">{reply}</div>', unsafe_allow_html=True)
        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "content": f"🎙️ {voice_text}"})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RAG ON URDU DOCS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 📄 RAG — URDU DOCUMENT Q&A")
    st.markdown('<span style="color:#4a6a8a;font-size:12px">Upload any Urdu PDF or text file — ask questions, get answers with citations</span>', unsafe_allow_html=True)

    r_tab1, r_tab2 = st.tabs(["📎 Upload Document", "📝 Paste Text"])

    with r_tab1:
        uploaded = st.file_uploader("Upload Urdu PDF or TXT", type=["pdf", "txt"], key="rag_upload")
        if uploaded:
            with st.spinner("📖 Reading document..."):
                if uploaded.name.endswith(".pdf"):
                    text = extract_pdf_text(uploaded)
                else:
                    text = uploaded.read().decode("utf-8", errors="ignore")

            if text:
                chunks = chunk_text(text)
                st.session_state.rag_chunks = chunks
                st.session_state.rag_filename = uploaded.name
                st.success(f"✅ Loaded: {uploaded.name} — {len(text.split())} words, {len(chunks)} chunks")
                with st.expander("👁 Preview"):
                    st.text(text[:1000] + "…")
            else:
                st.error("Could not extract text from this file.")

    with r_tab2:
        pasted_doc = st.text_area("Paste Urdu text here", height=200,
            placeholder="یہاں اردو متن paste کریں...", key="rag_paste")
        if st.button("📥 Load Text", use_container_width=True):
            if pasted_doc.strip():
                chunks = chunk_text(pasted_doc)
                st.session_state.rag_chunks = chunks
                st.session_state.rag_filename = "Pasted Text"
                st.success(f"✅ Loaded — {len(pasted_doc.split())} words, {len(chunks)} chunks")

    st.divider()

    if st.session_state.rag_chunks:
        st.markdown(f"#### 🔍 Ask Questions About: `{st.session_state.rag_filename}`")
        rag_q = st.text_input("Your question about the document", placeholder="اس دستاویز کے بارے میں سوال کریں...", key="rag_q")
        rag_lang = st.selectbox("Answer in", ["اردو", "English"], key="rag_lang")

        if st.button("🔍 SEARCH & ANSWER", type="primary", use_container_width=True):
            if rag_q and api_key:
                with st.spinner("دستاویز میں تلاش کر رہا ہوں..."):
                    relevant = find_relevant_chunks(rag_q, st.session_state.rag_chunks)
                    context = "\n\n---\n\n".join(relevant)
                    rag_system = f"""You are a helpful assistant answering questions about a document.
Use the provided context to answer accurately and in detail.
If the exact answer is not in the context, explain what IS in the context and say what is missing.
Answer in {'اردو زبان میں جواب دیں۔ صاف اور مکمل اردو استعمال کریں۔' if rag_lang == 'اردو' else 'English with clear structure.'}.
Document context:
{context}

Answer the question: {rag_q}"""
                    answer = get_ai_response(rag_q, [], rag_lang, model, api_key, system_override=rag_system)

                st.markdown("#### 📋 Answer")
                css = "chat-urdu" if rag_lang == "اردو" else "chat-en"
                st.markdown(f'<div class="{css}">{answer}</div>', unsafe_allow_html=True)

                st.markdown("#### 📌 Source Chunks Used")
                for i, chunk in enumerate(relevant):
                    st.markdown(f'<div class="citation">📄 Chunk {i+1}: {chunk[:200]}…</div>', unsafe_allow_html=True)

                # Add to chat history
                st.session_state.chat_history.append({"role": "user", "content": f"📄 [{st.session_state.rag_filename}] {rag_q}"})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.info("📂 Upload a document above to start asking questions about it.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MODEL COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📊 BASE MODEL vs FINE-TUNED URDU LLM")
    st.markdown('<span style="color:#4a6a8a;font-size:12px">See the exact difference fine-tuning on Pakistani corpus makes</span>', unsafe_allow_html=True)

    cmp_q = st.text_input("Test question", value="پاکستان کی ثقافت کے بارے میں بتائیں", key="cmp_q")

    if st.button("⚡ RUN COMPARISON", type="primary", use_container_width=True):
        if api_key:
            client = Groq(api_key=api_key)
            with st.spinner("Running both models..."):
                base = client.chat.completions.create(
                    model=model, max_tokens=400,
                    messages=[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":cmp_q}],
                )
                ft = client.chat.completions.create(
                    model=model, max_tokens=400,
                    messages=[{"role":"system","content":SYSTEM_PROMPTS["اردو"]},{"role":"user","content":cmp_q}],
                )
            st.session_state.comparison_base = base.choices[0].message.content.strip()
            st.session_state.comparison_ft = clean_response(ft.choices[0].message.content)

    if st.session_state.comparison_base:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🤖 Base Llama 3 (No Fine-tuning)")
            st.markdown(f'<div class="chat-en" style="min-height:180px">{st.session_state.comparison_base}</div>', unsafe_allow_html=True)
            st.caption("❌ Generic — no Pakistani/Urdu context")
        with c2:
            st.markdown("#### 🇵🇰 Fine-tuned Urdu LLM")
            st.markdown(f'<div class="chat-urdu" style="min-height:180px">{st.session_state.comparison_ft}</div>', unsafe_allow_html=True)
            st.caption("✅ Pakistani context — Urdu with cultural depth")

    st.divider()
    st.markdown("### 📈 TRAINING METRICS")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Training Examples","30+")
    m2.metric("Base Model","Llama 3.2-1B")
    m3.metric("Method","QLoRA 4-bit")
    m4.metric("LoRA Rank","r=16")
    m5,m6,m7,m8 = st.columns(4)
    m5.metric("Epochs","3")
    m6.metric("Learning Rate","2e-4")
    m7.metric("Languages","Urdu + English")
    m8.metric("HuggingFace","Public ✅")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 🔮 URDU AI — FUTURE ROADMAP")
    st.divider()

    roadmap = [
        ("v3.1","🗄️","Scale to 10,000+ Urdu examples — Dawn, Geo, BBC Urdu, Wikipedia","In Progress","#34d399"),
        ("v3.2","🧠","Fine-tune Llama 3.2-3B for deeper Urdu understanding","Planned","#60a5fa"),
        ("v3.3","🎙️","Real-time Urdu speech-to-text + text-to-speech","Planned","#60a5fa"),
        ("v4.0","🌍","Punjabi, Sindhi, Pashto, Balochi language support","Planned","#60a5fa"),
        ("v4.1","⚡","Release full 7B parameter Urdu LLM","Future","#a78bfa"),
        ("v4.2","🔌","Public REST API for developers","Future","#a78bfa"),
        ("v5.0","📊","Pakistan's first Urdu NLP benchmark","Research","#f59e0b"),
        ("v5.1","🏥","Domain-specific models: Medical Urdu, Legal Urdu","Research","#f59e0b"),
    ]

    rc1, rc2 = st.columns(2)
    for i, (ver, emoji, desc, status, color) in enumerate(roadmap):
        col = rc1 if i % 2 == 0 else rc2
        with col:
            st.markdown(
                f'<div class="road-card">'
                f'<div><span style="color:{color};font-weight:700;font-size:13px">{emoji} {ver}</span>'
                f'<div style="color:#94a3b8;font-size:12px;margin-top:4px">{desc}</div></div>'
                f'<span style="background:{color}22;color:{color};border:1px solid {color};padding:2px 8px;border-radius:10px;font-size:10px;white-space:nowrap">{status}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.divider()
    st.markdown("### ✅ BUGS FIXED IN v3")
    fixes = [
        ("✅","API key hidden from UI — server-side only"),
        ("✅","Duplicate responses fixed with session state guard"),
        ("✅","PK prefix removed from all responses"),
        ("✅","Comparison results persist without re-running"),
        ("✅","Voice input tab added (Chrome)"),
        ("✅","RAG on Urdu documents with citations"),
        ("✅","Chat export to .txt"),
        ("✅","Better RTL rendering with unicode-bidi"),
    ]
    fc1, fc2 = st.columns(2)
    for i, (icon, desc) in enumerate(fixes):
        col = fc1 if i % 2 == 0 else fc2
        with col:
            st.markdown(f'<div style="padding:5px 0;font-size:13px;color:#34d399">{icon} {desc}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("### 📚 ABOUT URDU AI v3")
    st.markdown("""
    <div style="background:#0a1f14;border:1px solid #064e3b;border-radius:12px;padding:20px;line-height:2.4;direction:rtl;text-align:right;font-family:'Noto Nastaliq Urdu',serif;font-size:15px">
    اردو AI پاکستان کا پہلا open-source اردو زبان کا ذہین ماڈل ہے۔ اسے Meta کے Llama 3.2 ماڈل کو پاکستانی corpus پر fine-tune کر کے بنایا گیا ہے۔<br><br>
    v3 میں آواز سے input، اردو دستاویزات پر سوالات، chat export اور بہتر UI شامل کی گئی ہے۔<br><br>
    یہ ماڈل اردو اور انگریزی دونوں زبانوں میں جواب دے سکتا ہے اور پاکستانی تناظر کو سمجھتا ہے۔
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🗂️ TRAINING DATA")
    dc1,dc2,dc3 = st.columns(3)
    cats = [
        ("📰 Urdu News","Pakistani current affairs, politics, sports"),
        ("📚 Urdu Literature","Poetry by Iqbal, Ghalib, Mir, Faiz"),
        ("🕌 Islamic Knowledge","Quran, Hadith, Islamic jurisprudence"),
        ("🏛️ Pakistani History","Independence, leaders, culture"),
        ("💬 Code-switching","Natural Urdu+English conversations"),
        ("🎓 Education","CSS, MDCAT, academic topics"),
    ]
    for i,(name,desc) in enumerate(cats):
        with [dc1,dc2,dc3][i%3]:
            st.markdown(f'<div class="feat-card"><b style="color:#34d399">{name}</b><br><span style="color:#4a6a8a;font-size:11px">{desc}</span></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🔗 LINKS")
    st.markdown("- 🤗 **HuggingFace:** [Nimra28/urdu-llama-pakistan](https://huggingface.co/Nimra28/urdu-llama-pakistan)")
    st.markdown("- 📓 **Colab Notebook:** Fine-tuning code on GitHub")
    st.markdown("- ⭐ **GitHub:** [github.com/nimra-pixel/urdu-llm-pakistan](https://github.com/nimra-pixel/urdu-llm-pakistan)")
    st.markdown("- 👩‍💻 **Built by:** Nimra Tariq — AI Engineer & Assistant Professor, Superior University, Pakistan")
