import os
from dotenv import load_dotenv

load_dotenv()

# Free local setup - no API keys needed
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"

DATA_FOLDER = "./data"
VECTORSTORE_PATH = "./vectorstore"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 5

# HuggingFace embedding model (free, runs locally)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Ollama local model (free, runs on your computer)
OLLAMA_MODEL = "tinyllama"
OLLAMA_BASE_URL = "http://localhost:11434"