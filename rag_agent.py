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
            chroma_path = os.path.abspath("./data/chroma_db")
            vectorstore = Chroma(
                persist_directory=chroma_path,
                collection_name="customer_support_kb",
                embedding_function=self.embeddings
            )
            
            # Retrieve relevant KB chunks
            docs = vectorstore.similarity_search(query, k=3)
            context = "\n\n".join([d.page_content for d in docs if len(d.page_content.strip()) > 30])
            
            if context.strip():
                # ✅ PERFECT RAG PROMPT - Uses retrieved context ONLY
                prompt = f"""SMARTSUPPORT CUSTOMER SUPPORT SPECIALIST

KNOWLEDGE BASE CONTEXT:
{context}

USER QUERY: {query}

INSTRUCTIONS:
1. Answer using ONLY the KB context above
2. Be SPECIFIC: Include URLs, exact steps, timelines, contact info
3. Professional, step-by-step guidance
4. If info missing: "Please contact support@smartsupport.com for assistance"
5. ALWAYS end response with: [RAG Agent]

PROVIDE STEP-BY-STEP SOLUTION:"""
                
                return self.llm.invoke(prompt).content
        
        except Exception as e:
            print(f"RAG Agent Error: {e}")
        return None
