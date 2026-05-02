# 📚 Document Q&A Bot — RAG Pipeline

A Retrieval-Augmented Generation (RAG) based Document Q&A Bot that allows users to ask natural language questions against a collection of documents and receive accurate, grounded answers with clear source citations.

---

## 🎯 What It Does

This bot ingests PDF, TXT, and DOCX documents, chunks and embeds them into a vector database, and uses a local LLM (Mistral via Ollama) to answer questions based **only** on the provided documents. Every answer includes the source filename and page number so users can verify the information.

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Core language |
| LangChain | 0.2+ | RAG pipeline orchestration |
| langchain-community | 0.2+ | Document loaders, vector store |
| langchain-core | 0.2+ | Prompts, runnables |
| langchain-text-splitters | 0.2+ | Text chunking |
| ChromaDB | 0.5+ | Vector database |
| sentence-transformers | 2.7+ | HuggingFace embeddings |
| Ollama | latest | Local LLM runner |
| Mistral 7B | latest | Answer generation LLM |
| Streamlit | 1.35+ | Web UI |
| PyPDF | 3.x | PDF text extraction |
| python-docx | 1.x | DOCX text extraction |
| python-dotenv | 1.x | Environment variables |

---

## 🏗️ Architecture Overview

```
User Question
     │
     ▼
┌─────────────────────────────────────────────┐
│              RAG PIPELINE                   │
│                                             │
│  1. INGESTION (ingest.py)                   │
│     └─ Load PDFs/TXT/DOCX from /data        │
│     └─ Extract clean text                   │
│     └─ Chunk text (500 chars, 100 overlap)  │
│     └─ Embed chunks (HuggingFace)           │
│     └─ Store in ChromaDB (persisted)        │
│                                             │
│  2. RETRIEVAL (retriever.py)                │
│     └─ Embed user query                     │
│     └─ Similarity search (top-k=5)          │
│     └─ Retrieve relevant chunks + metadata  │
│                                             │
│  3. GENERATION (retriever.py)               │
│     └─ Build prompt with context            │
│     └─ Send to Mistral via Ollama           │
│     └─ Return grounded answer + citations   │
└─────────────────────────────────────────────┘
     │
     ▼
Answer + Source Citations
```

---

## 📂 Project Structure

```
rag_qa_bot/
├── data/                          # Knowledge base documents
│   ├── artificial_intelligence_tutorial.pdf
│   ├── machine_learning_tutorial.pdf
│   ├── python_tutorial.pdf
│   ├── python_deep_learning_tutorial.pdf
│   └── data_science_tutorial.pdf
├── vectorstore/                   # Persisted ChromaDB vector store
├── app.py                         # Streamlit web UI
├── ingest.py                      # Document ingestion & indexing
├── retriever.py                   # Query retrieval & answer generation
├── main.py                        # CLI interactive loop
├── config.py                      # Configuration settings
├── .env                           # API keys (never committed)
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🔀 Chunking Strategy

**Strategy chosen: Recursive Character Text Splitting**

- **Chunk size:** 500 characters
- **Overlap:** 100 characters
- **Separators:** `["\n\n", "\n", " ", ""]`

**Why this strategy?**
Recursive Character Text Splitting was chosen because it respects natural text boundaries (paragraphs → sentences → words) before falling back to character splits. This preserves semantic coherence better than fixed-size chunking. The 100-character overlap ensures context is not lost at chunk boundaries, which is critical for multi-sentence answers.

---

## 🧠 Embedding Model

**Model: `all-MiniLM-L6-v2` (HuggingFace sentence-transformers)**

**Why?**
- Completely free — no API key required
- Runs locally on CPU
- Fast and lightweight (80MB)
- Strong semantic similarity performance for English text
- Batch embedding supported natively

---

## 🗄️ Vector Database

**Database: ChromaDB**

**Why?**
- Simple setup — no external server needed
- Persists to disk automatically
- Fast similarity search
- Native LangChain integration
- Ideal for local/offline RAG pipelines

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git
- Ollama installed ([download here](https://ollama.com/download))

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/rag_qa_bot.git
cd rag_qa_bot
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install langchain langchain-community langchain-core langchain-text-splitters langchain-openai chromadb pypdf python-docx python-dotenv sentence-transformers streamlit openai tiktoken
```

### Step 4 — Download Mistral Model via Ollama
```bash
# First start Ollama (it runs in background)
# Then pull the model:
ollama pull mistral
```

### Step 5 — Set Up Environment Variables
Create a `.env` file in the project root:
```
# No API keys needed for local setup!
USE_LOCAL_LLM=true
```

### Step 6 — Add Documents
Place your PDF, TXT, or DOCX files in the `/data` folder.

### Step 7 — Index Documents
```bash
python ingest.py
```

### Step 8 — Run the Web UI
```bash
streamlit run app.py
```

### Step 9 — OR Run CLI Version
```bash
python main.py
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_LOCAL_LLM` | No | Set to `true` for local Ollama (default) |
| `OPENAI_API_KEY` | No | Only if using OpenAI instead of Ollama |

> ⚠️ **Never commit your `.env` file or actual API keys to GitHub!**

---

## 💬 Example Queries & Expected Answers

| Query | Expected Answer Theme |
|-------|----------------------|
| "What is machine learning?" | Definition, types of ML, supervised/unsupervised learning |
| "What are Python data types?" | int, float, string, list, tuple, dict, set |
| "What is a neural network?" | Layers, neurons, activation functions, deep learning |
| "How is AI used in healthcare?" | Diagnosis, drug discovery, patient monitoring |
| "What is data preprocessing?" | Cleaning, normalization, handling missing values |
| "Who is the president of India?" | "I don't know based on provided documents" |

---

## ⚠️ Known Limitations

| Limitation | Reason |
|------------|--------|
| Slow first response (30-60 sec) | Mistral 7B runs locally on CPU — no GPU acceleration |
| Misspelled queries may miss context | Embedding model is sensitive to spelling |
| Hindi/other language queries answered in English | Documents are in English; LLM translates context |
| Large PDFs take longer to index | CPU-bound embedding generation |
| Cannot answer questions outside document scope | By design — grounded answers only |

---

## 🚀 Running the Project

```bash
# Terminal 1 — Make sure Ollama is running
ollama serve

# Terminal 2 — Run the app
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## 📸 Features

- ✅ Upload documents directly from the UI
- ✅ Clickable document list with suggested questions
- ✅ Source citations with filename and page number
- ✅ Handles irrelevant questions gracefully
- ✅ CLI and Web UI support
- ✅ Fully local — no internet needed after setup

---

*Built as part of AI Engineering Internship Assignment — RAG Pipeline*
