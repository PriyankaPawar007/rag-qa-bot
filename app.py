import streamlit as st
import os
import shutil
from ingest import main as index_documents
from retriever import ask_question

st.set_page_config(
    page_title="📚 DocBot",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 1px solid #00d4ff33;
}
.hero h1 { color: #00d4ff; font-size: 2.5rem; font-weight: 700; margin: 0; }
.hero p { color: #a0aec0; font-size: 1.1rem; margin-top: 10px; }

.tip-box {
    background: #1a2e1a;
    border: 1px solid #22c55e44;
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 15px 18px;
    color: #86efac;
    font-size: 0.9rem;
    margin: 10px 0;
    line-height: 1.8;
}

.doc-card {
    background: #1a1a2e;
    border: 1px solid #00d4ff33;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 6px 0;
    color: #e2e8f0;
    font-size: 0.9rem;
}
.doc-card-active {
    background: #1e3a5f;
    border: 2px solid #00d4ff;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 6px 0;
    color: #00d4ff;
    font-weight: 600;
    font-size: 0.9rem;
}

.answer-card {
    background: linear-gradient(135deg, #1a2744, #1e3a5f);
    border: 1px solid #00d4ff44;
    border-left: 4px solid #00d4ff;
    border-radius: 15px;
    padding: 20px 25px;
    margin: 15px 0;
    color: #e2e8f0;
    font-size: 1rem;
    line-height: 1.7;
}
.question-badge {
    background: #2d1b69;
    border: 1px solid #7c3aed;
    border-radius: 10px;
    padding: 10px 18px;
    color: #c4b5fd;
    font-weight: 600;
    margin-bottom: 10px;
}
.source-chip {
    background: #1a2e1a;
    border: 1px solid #22c55e44;
    border-radius: 8px;
    padding: 6px 14px;
    color: #86efac;
    font-size: 0.85rem;
    margin: 4px 2px;
    display: inline-block;
}
.upload-box {
    background: #1a1a2e;
    border: 2px dashed #00d4ff44;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin: 10px 0;
}
.stats-box {
    background: #1a1a2e;
    border: 1px solid #00d4ff22;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    color: #a0aec0;
}
.stats-number { color: #00d4ff; font-size: 1.8rem; font-weight: 700; }

.stTextInput > div > div > input {
    background: #1a1a2e !important;
    color: #e2e8f0 !important;
    border: 2px solid #00d4ff44 !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
}
.stTextInput > div > div > input:focus {
    border: 2px solid #00d4ff !important;
    box-shadow: 0 0 20px #00d4ff22 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #0066ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 30px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>📚 Document Q&A Bot</h1>
    <p>Upload your documents, select one, and ask questions instantly!</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# Load documents
DATA_FOLDER = "./data"
os.makedirs(DATA_FOLDER, exist_ok=True)
docs = [f for f in os.listdir(DATA_FOLDER) if f.endswith(('.pdf', '.txt', '.docx'))]

# Suggested questions
doc_suggestions = {
    "artificial_intelligence_tutorial.pdf": [
        "What is Artificial Intelligence?",
        "What are the types of AI?",
        "What is the history of AI?",
        "How is AI used in real life?",
    ],
    "machine_learning_tutorial.pdf": [
        "What is Machine Learning?",
        "What are supervised and unsupervised learning?",
        "What is overfitting in ML?",
        "What are common ML algorithms?",
    ],
    "python_tutorial.pdf": [
        "What are Python data types?",
        "How do functions work in Python?",
        "What are Python lists and tuples?",
        "What is OOP in Python?",
    ],
    "python_deep_learning_tutorial.pdf": [
        "What is deep learning?",
        "What is a neural network?",
        "What is backpropagation?",
        "How is deep learning different from ML?",
    ],
    "data_science_tutorial.pdf": [
        "What is data science?",
        "What tools are used in data science?",
        "What is data preprocessing?",
        "What is exploratory data analysis?",
    ],
}

# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ Control Panel")
    st.markdown("---")

    # ── TIPS ──
    with st.expander("💡 Tips & How to Use", expanded=False):
        st.markdown("""
        <div class="tip-box">
        📌 <b>How to use this app:</b><br><br>
        1️⃣ Upload your PDF/TXT/DOCX files below<br>
        2️⃣ Click <b>Index Documents</b> after uploading<br>
        3️⃣ Select a document from the list<br>
        4️⃣ Click a suggested question OR type your own<br>
        5️⃣ Press <b>Enter</b> or click <b>Ask</b><br><br>
        ⚡ <b>Shortcuts:</b><br>
        • Press <b>Enter</b> to submit question<br>
        • Click <b>Clear</b> to reset answers<br>
        • Click <b>Re-Index</b> after adding new files<br><br>
        ⚠️ <b>Note:</b> First answer may take 30-60 seconds
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── UPLOAD DOCUMENTS ──
    st.markdown("### 📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Drop your files here",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="Upload PDF, TXT, or DOCX files to add to your knowledge base"
    )

    if uploaded_files:
        saved_count = 0
        for uploaded_file in uploaded_files:
            save_path = os.path.join(DATA_FOLDER, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_count += 1
        st.success(f"✅ {saved_count} file(s) uploaded successfully!")
        st.info("👇 Click **Index Documents** to make them searchable!")
        docs = [f for f in os.listdir(DATA_FOLDER) if f.endswith(('.pdf', '.txt', '.docx'))]

    st.markdown("---")

    # ── INDEX BUTTON ──
    if st.button("🔄 Index Documents", use_container_width=True):
        with st.spinner("⏳ Indexing... please wait (2-3 mins first time)"):
            try:
                index_documents()
                st.success("✅ Indexing complete!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ {str(e)}")

    st.markdown("---")

    # ── DOCUMENT LIST ──
    st.markdown("### 📁 Documents")
    if docs:
        for doc in docs:
            is_active = st.session_state.selected_doc == doc
            emoji = "📕" if doc.endswith(".pdf") else ("📝" if doc.endswith(".txt") else "📘")
            label = f"{'✅' if is_active else emoji} {doc}"
            if st.button(label, key=f"doc_{doc}", use_container_width=True):
                st.session_state.selected_doc = doc
                st.rerun()
    else:
        st.warning("⚠️ No documents found! Upload some above.")

    st.markdown("---")

    # ── STATS ──
    st.markdown("### 📊 Stats")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<div class="stats-box"><div class="stats-number">{len(docs)}</div>📄 Docs</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="stats-box"><div class="stats-number">{len(st.session_state.messages)}</div>💬 Asked</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── DELETE DOCUMENTS ──
    with st.expander("🗑️ Manage Documents", expanded=False):
        if docs:
            doc_to_delete = st.selectbox("Select file to delete:", docs)
            if st.button("❌ Delete Selected File", use_container_width=True):
                os.remove(os.path.join(DATA_FOLDER, doc_to_delete))
                if st.session_state.selected_doc == doc_to_delete:
                    st.session_state.selected_doc = None
                st.success(f"Deleted {doc_to_delete}")
                st.rerun()
        else:
            st.info("No documents to manage.")

# ─── MAIN CONTENT ───────────────────────────────────────────
if st.session_state.selected_doc:
    selected = st.session_state.selected_doc
    st.markdown(f"### 📖 Exploring: `{selected}`")

    suggestions = doc_suggestions.get(selected, [
        "What is the main topic of this document?",
        "Summarize the key points",
        "What are the important concepts?",
        "Give me examples from this document",
    ])

    st.markdown("**💡 Suggested Questions — click to ask instantly:**")
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(f"💬 {suggestion}", key=f"sug_{i}", use_container_width=True):
                with st.spinner("🤔 Thinking..."):
                    try:
                        answer, sources = ask_question(suggestion)
                        st.session_state.messages.append({
                            "question": suggestion,
                            "answer": answer,
                            "sources": sources
                        })
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
    st.markdown("---")
else:
    st.markdown("### 👈 Select a document from the sidebar to get started!")
    st.markdown("Or just type any question below.")
    st.markdown("---")

# ── QUESTION INPUT ──
st.markdown("### ✏️ Ask Any Question")
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    question = st.text_input(
        "",
        placeholder="💬 Type your question and press Enter...",
        key="q_input",
        label_visibility="collapsed"
    )
with col2:
    ask_btn = st.button("🔍 Ask", use_container_width=True)
with col3:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Process question
if question and question.strip() and len(question.strip()) >= 2:
    already_answered = (
        st.session_state.messages and
        st.session_state.messages[-1]["question"] == question
    )
    if not already_answered:
        if not any(c.isalpha() for c in question):
            st.warning("⚠️ Please enter a valid question with actual words!")
        else:
            with st.spinner("🤔 Searching documents and generating answer..."):
                try:
                    answer, sources = ask_question(question)
                    st.session_state.messages.append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"❌ {str(e)}")

# ── ANSWERS ──
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 📝 Answers")
    for chat in reversed(st.session_state.messages):
        st.markdown(
            f'<div class="question-badge">🙋 {chat["question"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="answer-card">🤖 <b>Answer:</b><br><br>{chat["answer"]}</div>',
            unsafe_allow_html=True
        )
        if chat["sources"]:
            sources_html = "".join([
                f'<span class="source-chip">📄 {s}</span>'
                for s in chat["sources"]
            ])
            st.markdown(
                f'<div style="margin:10px 0">📚 <b>Sources:</b><br>{sources_html}</div>',
                unsafe_allow_html=True
            )
        st.markdown("<hr style='border-color:#ffffff11'>", unsafe_allow_html=True)