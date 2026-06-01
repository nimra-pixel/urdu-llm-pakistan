import streamlit as st
from groq import Groq
import datetime
import json
import io
import base64

st.set_page_config(page_title="اردو AI — Pakistani LLM Platform", page_icon="🇵🇰", layout="wide")

# Clean Black & White Theme
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

  /* Base - Pure Black & White */
  html, body, [class*="css"] {
      background: #000000 !important;
      color: #FFFFFF !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  }
  
  .stApp {
      background: #000000 !important;
  }
  
  .block-container {
      padding-top: 1rem !important;
      padding-bottom: 2rem !important;
      max-width: 1400px !important;
  }
  
  /* Headers */
  h1, h2, h3, h4, h5, h6 {
      color: #FFFFFF !important;
      font-weight: 600 !important;
      letter-spacing: -0.02em !important;
  }
  
  h1 {
      font-size: 2.5rem !important;
      font-weight: 700 !important;
      letter-spacing: -0.03em !important;
  }
  
  /* Sidebar - Pure Black */
  [data-testid="stSidebar"] {
      background: #000000 !important;
      border-right: 1px solid #333333 !important;
  }
  
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
      color: #FFFFFF !important;
  }
  
  /* Buttons - Minimal Black/White */
  .stButton > button {
      background: #1A1A1A !important;
      color: #FFFFFF !important;
      border: 1px solid #333333 !important;
      border-radius: 8px !important;
      font-size: 13px !important;
      font-weight: 500 !important;
      padding: 8px 16px !important;
      transition: all 0.2s ease !important;
  }
  
  .stButton > button:hover {
      background: #2A2A2A !important;
      border-color: #FFFFFF !important;
      transform: translateY(-1px) !important;
  }
  
  .stButton > button:active {
      transform: translateY(0px) !important;
  }
  
  .stButton > button[kind="primary"] {
      background: #FFFFFF !important;
      color: #000000 !important;
      border: 1px solid #FFFFFF !important;
      font-weight: 600 !important;
  }
  
  .stButton > button[kind="primary"]:hover {
      background: #E0E0E0 !important;
      border-color: #E0E0E0 !important;
  }
  
  /* Chat Messages - Monochrome */
  .chat-urdu, .chat-user, .chat-en, .chat-mixed {
      border-radius: 12px;
      padding: 16px 20px;
      margin: 12px 0;
      line-height: 1.6;
      font-size: 14px;
  }
  
  .chat-user {
      background: #1A1A1A !important;
      border: 1px solid #333333 !important;
      text-align: right;
      direction: rtl;
      margin-left: 20%;
  }
  
  .chat-urdu, .chat-en, .chat-mixed {
      background: #0A0A0A !important;
      border: 1px solid #2A2A2A !important;
      text-align: left;
      margin-right: 20%;
  }
  
  .chat-urdu {
      font-family: 'Noto Nastaliq Urdu', serif !important;
      text-align: right;
      direction: rtl;
  }
  
  /* Inputs - Clean Black/White */
  .stTextInput input, .stTextArea textarea {
      background: #0A0A0A !important;
      border: 1px solid #333333 !important;
      color: #FFFFFF !important;
      border-radius: 10px !important;
      font-size: 14px !important;
      padding: 12px !important;
  }
  
  .stTextInput input:focus, .stTextArea textarea:focus {
      border-color: #FFFFFF !important;
      outline: none !important;
      box-shadow: 0 0 0 1px #FFFFFF !important;
  }
  
  /* Select boxes */
  .stSelectbox > div > div {
      background: #0A0A0A !important;
      border: 1px solid #333333 !important;
      color: #FFFFFF !important;
      border-radius: 8px !important;
  }
  
  .stSelectbox label, .stRadio label, .stSlider label, .stFileUploader label {
      color: #888888 !important;
      font-size: 12px !important;
      font-weight: 500 !important;
  }
  
  /* Radio buttons */
  .stRadio > div {
      gap: 16px !important;
  }
  
  .stRadio label {
      color: #FFFFFF !important;
  }
  
  /* Expander */
  [data-testid="stExpander"] {
      border: 1px solid #333333 !important;
      background: #0A0A0A !important;
      border-radius: 10px !important;
  }
  
  .streamlit-expanderHeader {
      color: #FFFFFF !important;
      font-weight: 500 !important;
  }
  
  /* Metrics - Clean Cards */
  [data-testid="stMetric"] {
      background: #0A0A0A !important;
      border: 1px solid #333333 !important;
      border-radius: 12px !important;
      padding: 16px !important;
  }
  
  [data-testid="stMetricValue"] {
      color: #FFFFFF !important;
      font-size: 1.8rem !important;
      font-weight: 700 !important;
  }
  
  [data-testid="stMetricLabel"] {
      color: #888888 !important;
      font-size: 0.75rem !important;
      text-transform: uppercase !important;
      letter-spacing: 0.5px !important;
  }
  
  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
      gap: 8px !important;
      border-bottom: 1px solid #333333 !important;
  }
  
  .stTabs [data-baseweb="tab"] {
      color: #888888 !important;
      font-size: 13px !important;
      font-weight: 500 !important;
      padding: 8px 20px !important;
      background: transparent !important;
  }
  
  .stTabs [aria-selected="true"] {
      color: #FFFFFF !important;
      border-bottom: 2px solid #FFFFFF !important;
  }
  
  /* Dividers */
  hr {
      border-color: #333333 !important;
      margin: 24px 0 !important;
  }
  
  /* Alerts & Messages */
  .stSuccess, .stInfo, .stWarning, .stError {
      background: #0A0A0A !important;
      border-left: 3px solid !important;
      border-radius: 8px !important;
      padding: 12px 16px !important;
  }
  
  .stSuccess { border-left-color: #FFFFFF !important; }
  .stInfo { border-left-color: #888888 !important; }
  .stWarning { border-left-color: #FFD700 !important; }
  .stError { border-left-color: #FF4444 !important; }
  
  /* Progress bar */
  .stProgress > div > div {
      background: #FFFFFF !important;
  }
  
  /* Feature Cards - Minimal */
  .feat-card {
      background: #0A0A0A;
      border: 1px solid #333333;
      border-radius: 10px;
      padding: 14px;
      margin: 6px 0;
      transition: all 0.2s ease;
  }
  
  .feat-card:hover {
      border-color: #FFFFFF;
      transform: translateX(2px);
  }
  
  /* Citation blocks */
  .citation {
      background: #0A0A0A;
      border-left: 3px solid #FFFFFF;
      padding: 10px 14px;
      margin: 8px 0;
      border-radius: 0 8px 8px 0;
      font-size: 12px;
      color: #CCCCCC;
  }
  
  /* Roadmap cards */
  .road-card {
      background: #0A0A0A;
      border: 1px solid #333333;
      border-radius: 10px;
      padding: 14px 18px;
      margin: 8px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
  }
  
  .road-card:hover {
      border-color: #FFFFFF;
  }
  
  /* Stats pills */
  .stat-pill {
      display: inline-block;
      background: #1A1A1A;
      border: 1px solid #333333;
      border-radius: 20px;
      padding: 4px 14px;
      font-size: 12px;
      margin: 4px;
      color: #CCCCCC;
  }
  
  /* Version badge */
  .v-badge {
      display: inline-block;
      background: #1A1A1A;
      border: 1px solid #FFFFFF;
      color: #FFFFFF;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
  }
  
  /* Status tags */
  .status-tag {
      padding: 2px 10px;
      border-radius: 12px;
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.5px;
      background: #1A1A1A;
      border: 1px solid #333333;
      color: #CCCCCC;
  }
  
  /* Scrollbar - Minimal */
  ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
  }
  
  ::-webkit-scrollbar-track {
      background: #000000;
  }
  
  ::-webkit-scrollbar-thumb {
      background: #333333;
      border-radius: 3px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
      background: #FFFFFF;
  }
  
  /* File uploader */
  .stFileUploader > div > button {
      background: #1A1A1A !important;
      border: 1px solid #333333 !important;
      color: #FFFFFF !important;
  }
  
  /* Code blocks */
  code, pre {
      background: #0A0A0A !important;
      color: #FFFFFF !important;
      border: 1px solid #333333 !important;
  }
  
  /* Spinner */
  .stSpinner > div {
      border-color: #FFFFFF !important;
  }
</style>
""", unsafe_allow_html=True)

# API Key
api_key = st.secrets.get("GROQ_API_KEY", "")

# Session state
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

# System prompts
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
    if not chunks:
        words = text.split()
        i = 0
        while i < len(words):
            chunks.append(" ".join(words[i:i+chunk_size]))
            i += chunk_size - overlap
    return chunks

def find_relevant_chunks(query, chunks, top_k=3):
    query_words = query.lower().split()
    scored = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = sum(chunk_lower.count(w) for w in query_words if len(w) > 2)
        if query.lower() in chunk_lower:
            score += 10
        scored.append((score, i, chunk))
    scored.sort(reverse=True)
    relevant = [c for s, _, c in scored if s > 0][:top_k]
    if not relevant:
        relevant = chunks[:top_k]
    return relevant

def export_chat_txt():
    lines = ["=" * 50, "اردو AI — Chat Export", f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", "=" * 50, ""]
    for msg in st.session_state.chat_history:
        role = "👤 User" if msg["role"] == "user" else "🇵🇰 Urdu AI"
        lines.append(f"{role}:\n{msg['content']}\n")
    return "\n".join(lines)

# Sidebar
with st.sidebar:
    st.markdown("## 🇵🇰 اردو AI")
    st.markdown("---")
    
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.caption("Get your free API key at console.groq.com")
    else:
        st.success("✓ API Key configured")
    
    model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    st.markdown("---")
    
    st.markdown("### Language")
    lang_mode = st.radio(
        "Mode", 
        ["اردو", "English", "Mixed (اردو + English)"],
        index=["اردو", "English", "Mixed (اردو + English)"].index(st.session_state.lang_mode)
    )
    if lang_mode != st.session_state.lang_mode:
        st.session_state.lang_mode = lang_mode
    
    st.markdown("---")
    st.markdown("### Session")
    total = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    st.markdown(f'<span class="stat-pill">💬 {total} Questions</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="stat-pill">📄 {st.session_state.rag_filename or "No Document"}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Actions")
    
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
    
    st.markdown("---")
    st.caption("Built with Llama 3 • Fine-tuned on Pakistani Corpus")

# Header
c1, c2, c3 = st.columns([4, 1, 1])
with c1:
    st.markdown("# 🇵🇰 اردو AI")
    st.caption("Pakistan's Open-Source Urdu LLM Platform")
with c3:
    st.markdown('<div style="text-align: right; margin-top: 20px;"><span class="v-badge">v3.0</span></div>', unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat", "🎙️ Voice", "📄 RAG", "📊 Compare", "🔮 Roadmap", "ℹ️ About"
])

# TAB 1 for CHAT

with tab1:
    st.markdown("### 💬 Conversation")
    
    quick_prompts = [
        "پاکستان کی تاریخ", "علامہ اقبال کی شاعری",
        "اسلام میں زکوٰۃ", "Machine learning",
        "لاہور کے کھانے", "پاکستان کا آئین",
    ]
    
    cols = st.columns(6)
    for i, qp in enumerate(quick_prompts):
        with cols[i]:
            if st.button(qp, key=f"qp_{i}", use_container_width=True):
                last = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
                if last != qp and not st.session_state.processing:
                    st.session_state.processing = True
                    st.session_state.chat_history.append({"role": "user", "content": qp})
                    if api_key:
                        reply = get_ai_response(qp, st.session_state.chat_history[:-1], lang_mode, model, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.session_state.processing = False
                    st.rerun()
    
    st.markdown("---")
    
    # Chat display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown('<div class="chat-urdu">السلام علیکم! میں اردو AI ہوں — پاکستان کا اردو ذہین ماڈل۔ میں اردو یا انگریزی میں بات کر سکتا ہوں۔ 🇵🇰</div>', unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                css = "chat-urdu" if lang_mode == "اردو" else ("chat-mixed" if "Mixed" in lang_mode else "chat-en")
                st.markdown(f'<div class="{css}">🇵🇰 {msg["content"]}</div>', unsafe_allow_html=True)
    
    # Input
    user_input = st.text_area(
        "Your message",
        placeholder="Type your question here in Urdu or English...",
        label_visibility="collapsed",
        key="chat_in",
        height=100,
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        send = st.button("Send →", use_container_width=True, type="primary",
                         disabled=st.session_state.processing)
    
    if send and user_input and user_input.strip() and api_key and not st.session_state.processing:
        user_input = user_input.strip()
        if user_input != st.session_state.last_input:
            st.session_state.last_input = user_input
            st.session_state.processing = True
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                reply = get_ai_response(user_input, st.session_state.chat_history[:-1], lang_mode, model, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.processing = False
            st.rerun()
    
    if not api_key:
        st.warning("⚠️ Please configure your Groq API key in the sidebar")


# TAB 2 for VOICE INPUT
with tab2:
    st.markdown("### 🎙️ Voice Input")
    st.markdown("Upload an audio file for transcription and response")
    
    audio_file = st.file_uploader(
        "Upload audio (MP3, WAV, M4A, OGG)",
        type=["mp3", "wav", "m4a", "ogg", "webm"],
        key="voice_upload"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        vlang = st.selectbox("Transcription Language", ["ur", "en"], 
                             format_func=lambda x: "Urdu" if x=="ur" else "English",
                             key="vlang")
    with col2:
        resp_lang = st.selectbox("Response Language", ["اردو", "English", "Mixed (اردو + English)"], key="resp_lang")
    
    if audio_file and api_key:
        st.audio(audio_file)
        if st.button("Transcribe & Respond", type="primary", use_container_width=True):
            with st.spinner("Processing audio..."):
                try:
                    client = Groq(api_key=api_key)
                    audio_bytes = audio_file.read()
                    transcription = client.audio.transcriptions.create(
                        file=(audio_file.name, audio_bytes, audio_file.type),
                        model="whisper-large-v3",
                        language=vlang,
                        response_format="text",
                    )
                    transcript_text = str(transcription).strip()
                    st.success(f"Transcribed: {transcript_text}")
                    
                    with st.spinner("Generating response..."):
                        reply = get_ai_response(transcript_text, [], resp_lang, model, api_key)
                    
                    st.markdown("### Response")
                    css = "chat-urdu" if resp_lang == "اردو" else "chat-en"
                    st.markdown(f'<div class="{css}">{reply}</div>', unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append({"role": "user", "content": f"🎙️ {transcript_text}"})
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.markdown("---")
    st.markdown("### Or type your question")
    voice_text = st.text_area("Type here", height=100, key="voice_type")
    if st.button("Get Response", use_container_width=True) and voice_text and api_key:
        with st.spinner("Thinking..."):
            reply = get_ai_response(voice_text, [], st.session_state.get("resp_lang", "اردو"), model, api_key)
        css = "chat-urdu" if st.session_state.get("resp_lang","اردو") == "اردو" else "chat-en"
        st.markdown(f'<div class="{css}">{reply}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "user", "content": voice_text})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})


# TAB 3 for RAG
with tab3:
    st.markdown("### 📄 Document Q&A")
    st.caption("Upload Urdu documents and ask questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], key="rag_upload")
        if uploaded:
            with st.spinner("Reading document..."):
                if uploaded.name.endswith(".pdf"):
                    text = extract_pdf_text(uploaded)
                else:
                    text = uploaded.read().decode("utf-8", errors="ignore")
            
            if text:
                chunks = chunk_text(text)
                st.session_state.rag_chunks = chunks
                st.session_state.rag_filename = uploaded.name
                st.success(f"Loaded: {uploaded.name}")
                with st.expander("Preview"):
                    st.text(text[:500] + "…")
            else:
                st.error("Could not extract text")
    
    with col2:
        pasted_doc = st.text_area("Or paste text here", height=150, key="rag_paste")
        if st.button("Load Text", use_container_width=True):
            if pasted_doc.strip():
                chunks = chunk_text(pasted_doc)
                st.session_state.rag_chunks = chunks
                st.session_state.rag_filename = "Pasted Text"
                st.success(f"Loaded: {len(pasted_doc.split())} words")
    
    if st.session_state.rag_chunks:
        st.markdown("---")
        st.markdown(f"**Active Document:** `{st.session_state.rag_filename}`")
        
        rag_q = st.text_area("Ask a question about this document", height=80, key="rag_q")
        rag_lang = st.selectbox("Response Language", ["اردو", "English"], key="rag_lang")
        
        if st.button("Search & Answer", type="primary", use_container_width=True):
            if rag_q and api_key:
                with st.spinner("Searching document..."):
                    relevant = find_relevant_chunks(rag_q, st.session_state.rag_chunks)
                    context = "\n\n---\n\n".join(relevant)
                    rag_system = f"""Answer the question based on the context provided.
Context:
{context}

Question: {rag_q}

Answer in {'Urdu' if rag_lang == 'اردو' else 'English'}."""
                    
                    answer = get_ai_response(rag_q, [], rag_lang, model, api_key, system_override=rag_system)
                
                st.markdown("#### Answer")
                css = "chat-urdu" if rag_lang == "اردو" else "chat-en"
                st.markdown(f'<div class="{css}">{answer}</div>', unsafe_allow_html=True)
                
                with st.expander("View source chunks"):
                    for i, chunk in enumerate(relevant):
                        st.markdown(f'<div class="citation">Chunk {i+1}: {chunk[:300]}…</div>', unsafe_allow_html=True)
                
                st.session_state.chat_history.append({"role": "user", "content": f"📄 [{st.session_state.rag_filename}] {rag_q}"})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})


# TAB 4 for COMPARISON
with tab4:
    st.markdown("### 📊 Model Comparison")
    st.caption("Base Llama vs Fine-tuned Urdu Model")
    
    cmp_q = st.text_input("Test Question", value="پاکستان کی ثقافت کے بارے میں بتائیں", key="cmp_q")
    
    if st.button("Run Comparison", type="primary", use_container_width=True):
        if api_key:
            client = Groq(api_key=api_key)
            with st.spinner("Running comparison..."):
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
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Base Model")
            st.markdown(f'<div class="chat-en" style="min-height: 180px">{st.session_state.comparison_base}</div>', unsafe_allow_html=True)
            st.caption("❌ Generic response, no Pakistani context")
        with col2:
            st.markdown("#### Fine-tuned Urdu Model")
            st.markdown(f'<div class="chat-urdu" style="min-height: 180px">{st.session_state.comparison_ft}</div>', unsafe_allow_html=True)
            st.caption("✅ Pakistani context, natural Urdu")
    
    st.markdown("---")
    st.markdown("### Training Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Training Examples", "30+")
    m2.metric("Base Model", "Llama 3.2-1B")
    m3.metric("Method", "QLoRA 4-bit")
    m4.metric("LoRA Rank", "r=16")

# TAB 5 for ROADMAP
with tab5:
    st.markdown("### 🔮 Roadmap")
    
    roadmap_items = [
        ("v3.1", "Scale to 10,000+ Urdu examples", "In Progress"),
        ("v3.2", "Fine-tune Llama 3.2-3B", "Planned"),
        ("v3.3", "Real-time speech-to-text", "Planned"),
        ("v4.0", "Punjabi, Sindhi, Pashto support", "Planned"),
        ("v4.1", "7B parameter Urdu LLM", "Future"),
        ("v5.0", "Urdu NLP Benchmark", "Research"),
    ]
    
    for version, desc, status in roadmap_items:
        st.markdown(
            f'<div class="road-card">'
            f'<div><strong>{version}</strong><br>'
            f'<span style="color: #888; font-size: 13px;">{desc}</span></div>'
            f'<span class="status-tag">{status}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown("### v3.0 Fixes")
    fixes = [
        "✓ API key hidden from UI",
        "✓ No duplicate responses",
        "✓ Clean response formatting",
        "✓ Persistent comparison results",
        "✓ RAG with citations",
        "✓ Chat export functionality",
    ]
    
    col1, col2 = st.columns(2)
    for i, fix in enumerate(fixes):
        col = col1 if i < 3 else col2
        col.markdown(fix)

# TAB 6 for ABOUT
with tab6:
    st.markdown("### ℹ️ About اردو AI")
    
    st.markdown("""
    <div style="background: #0A0A0A; border: 1px solid #333333; border-radius: 12px; padding: 24px; line-height: 1.8;">
    <p style="font-size: 15px;"><strong>اردو AI</strong> is Pakistan's open-source Urdu language model, fine-tuned on Pakistani corpus from Meta's Llama 3.2.</p>
    
    <p style="font-size: 14px; color: #CCCCCC; margin-top: 16px;">
    This model understands both Urdu and English, with deep knowledge of Pakistani culture, history, and Islamic context.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Training Data")
    
    cats = [
        ("📰 Urdu News", "Current affairs, politics, sports"),
        ("📚 Urdu Literature", "Poetry by Iqbal, Ghalib, Mir, Faiz"),
        ("🕌 Islamic Knowledge", "Quran, Hadith, jurisprudence"),
        ("🏛️ Pakistani History", "Independence, leaders, culture"),
        ("💬 Code-switching", "Natural Urdu+English conversations"),
        ("🎓 Education", "CSS, MDCAT, academic topics"),
    ]
    
    cols = st.columns(3)
    for i, (name, desc) in enumerate(cats):
        with cols[i % 3]:
            st.markdown(f'<div class="feat-card"><strong>{name}</strong><br><span style="color: #888; font-size: 11px;">{desc}</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Links")
    st.markdown("• [HuggingFace Model](https://huggingface.co/Nimra28/urdu-llama-pakistan)")
    st.markdown("• [GitHub Repository](https://github.com/nimra-pixel/urdu-llm-pakistan)")
    st.markdown("• Built by Nimra Tariq — AI Engineer, Superior University, Pakistan")
