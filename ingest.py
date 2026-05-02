import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import DATA_FOLDER, VECTORSTORE_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def load_documents():
    documents = []
    if not os.path.exists(DATA_FOLDER):
        print(f"Please create folder: {DATA_FOLDER} and add your PDFs")
        return documents
    for filename in os.listdir(DATA_FOLDER):
        filepath = os.path.join(DATA_FOLDER, filename)
        print(f"Loading {filename}...")
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding='utf-8')
            documents.extend(loader.load())
        elif filename.endswith(".docx"):
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(filepath)
            documents.extend(loader.load())
    print(f"Total pages loaded: {len(documents)}")
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def create_vectorstore(chunks):
    print("Creating embeddings (first time takes 2-3 minutes)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_PATH
    )
    print(f"✅ Vector database saved!")
    return vectorstore

def main():
    print("🚀 Starting document indexing...")
    documents = load_documents()
    if not documents:
        print("❌ No documents found! Add PDFs to the /data folder first.")
        return
    chunks = chunk_documents(documents)
    create_vectorstore(chunks)
    print("✅ Indexing complete! You can now run the app.")

if __name__ == "__main__":
    main()