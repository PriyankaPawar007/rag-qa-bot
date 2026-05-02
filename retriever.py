from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import VECTORSTORE_PATH, TOP_K_RESULTS, OLLAMA_MODEL, OLLAMA_BASE_URL

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )
    return vectorstore

def ask_question(question):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K_RESULTS})
    
    docs = retriever.invoke(question)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt_template = """You are a helpful assistant. Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know based on the provided documents."

Context:
{context}

Question: {question}

Answer:"""

    llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1
    )

    prompt = prompt_template.format(context=context, question=question)
    answer = llm.invoke(prompt)
    
    sources = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        sources.append(f"📄 {source} — Page {page}")
    
    return answer, list(set(sources))