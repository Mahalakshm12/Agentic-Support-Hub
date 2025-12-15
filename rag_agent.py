import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

class RAGAgent:
    def __init__(self):
        self.name = "RAG Agent (Customer Support)"
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )
    
    def execute(self, query: str) -> str:
        try:
            # ✅ FIX 1: ABSOLUTE PATH - Works in Streamlit + Terminal
            chroma_path = os.path.join(os.path.dirname(__file__), "data", "chroma_db")
            chroma_path = os.path.abspath(chroma_path)
            
            print(f"🔍 Loading ChromaDB from: {chroma_path}")
            
            # ✅ FIX 2: Check if ChromaDB exists
            if not os.path.exists(chroma_path):
                return "❌ ChromaDB not found. Run `python init_db.py` first. [RAG Agent]"
            
            vectorstore = Chroma(
                persist_directory=chroma_path,
                collection_name="customer_support_kb",
                embedding_function=self.embeddings
            )
            
            # Retrieve relevant KB chunks
            docs = vectorstore.similarity_search(query, k=3)
            context_docs = [d.page_content for d in docs if len(d.page_content.strip()) > 30]
            context = "\n\n".join(context_docs)
            
            print(f"📚 Found {len(context_docs)} relevant docs")
            
            if context.strip():
                prompt = f"""SMARTSUPPORT CUSTOMER SUPPORT SPECIALIST

KNOWLEDGE BASE CONTEXT:
{context}

USER QUERY: {query}

INSTRUCTIONS:
1. Answer using ONLY the KB context above
2. Be SPECIFIC: Include URLs, exact steps, timelines, contact info
3. Professional, step-by-step guidance
4. If info missing: "Please contact [support@smartsupport.com](mailto:support@smartsupport.com) for assistance"
5. ALWAYS end response with: [RAG Agent]

PROVIDE STEP-BY-STEP SOLUTION:"""
                
                response = self.llm.invoke(prompt).content
                return response.strip() + " [RAG Agent]"
            else:
                return "No relevant information found in knowledge base. Please contact [support@smartsupport.com](mailto:support@smartsupport.com) [RAG Agent]"
        
        except Exception as e:
            print(f"RAG Agent Error: {e}")
            return f"Error accessing knowledge base: {str(e)}. Please contact support. [RAG Agent]"

