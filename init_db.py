import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def create_vectorstore():
    print("📥 Loading knowledge base...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    kb_path = os.path.join("data", "knowledge_base.txt")
    chroma_dir = os.path.abspath(os.path.join("data", "chroma_db"))

    with open(kb_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.create_documents([text])

    os.makedirs(os.path.dirname(chroma_dir), exist_ok=True)

    Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=chroma_dir,
        collection_name="customer_support_kb",  # simple, valid name
    )
    print("✅ Vector store ready!")

if __name__ == "__main__":
    create_vectorstore()