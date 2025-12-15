import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from rag_agent import RAGAgent
from search_agent import SearchAgent

load_dotenv()

class SmartSupportMaster:
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.search_agent = SearchAgent()
        self.router_llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )
        print("🤖 Master Agent: BULLETPROOF ROUTER Ready! ✅")

    def select_agent(self, query: str) -> str:
        """Simple keyword router - NO LLM cost"""
        query_lower = query.lower()
        rag_keywords = ['password', 'reset', 'support', 'account', 'billing', 'order', 'shipping', 'escalate']
        if any(word in query_lower for word in rag_keywords):
            return "RAG_AGENT"
        return "SEARCH_AGENT"

    def _safe_execute(self, agent, query: str, agent_name: str) -> str:
        """🔧 BULLETPROOF: Handles ANY agent response"""
        try:
            # Call agent
            result = agent.execute(query)
            
            # ✅ FIX: Always return string + tag
            if result is None:
                return f"No response from {agent_name}. Please try again. [{agent_name}]"
            
            result_str = str(result).strip()
            if result_str:
                # Add tag if missing
                if agent_name not in result_str:
                    return f"{result_str}\n[{agent_name}]"
                return result_str
            else:
                return f"No relevant information found. [{agent_name}]"
                
        except Exception as e:
            return f"Error in {agent_name}: {str(e)} [{agent_name}]"

    def route_and_execute(self, query: str) -> str:
        """🔥 SIMPLE ROUTER - NO HYBRID (your request)"""
        print(f"\n🔍 ROUTING: '{query}'")
        
        agent = self.select_agent(query)
        print(f"   → {agent}")
        
        if agent == "RAG_AGENT":
            result = self._safe_execute(self.rag_agent, query, "RAG Agent")
            return result
        else:
            result = self._safe_execute(self.search_agent, query, "Search Agent")
            return result

if __name__ == "__main__":
    master = SmartSupportMaster()
    while True:
        query = input("\n👤 You: ")
        if query.lower() in ["quit", "exit"]:
            break
        print(master.route_and_execute(query))

