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

        # LLM used ONLY for routing decisions
        self.router_llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )

        print("🤖 Master Agent: TRUE AGENTIC ROUTER Ready!")

    def select_agent(self, query: str) -> str:
        """
        LLM-based intent router.
        NO keyword hacks.
        Routes to RAG only when internal intent is explicit.
        """

        router_prompt = """
You are a MASTER ROUTER AGENT for a CUSTOMER SUPPORT SYSTEM.

Your job is to decide which agent should answer the user's question.

AVAILABLE AGENTS:

1. RAG_AGENT
- Use ONLY if the question is CLEARLY about this company's product or support
- Examples:
  - Reset my SmartSupport password
  - Cancel my subscription
  - Track my order
  - Billing failed
  - Contact SmartSupport support
  - Warranty or refund policy

2. SEARCH_AGENT
- Use for ALL other questions, including:
  - General knowledge
  - World facts
  - Educational topics
  - How-to guides for public services
  - Email, Gmail, Netflix, Google, Windows, Apple, etc.

STRICT RULES:
- Do NOT assume internal intent just because the query mentions
  "account", "email", "password", or "login"
- If the company or product is NOT explicitly mentioned → SEARCH_AGENT
- If the question is general or informational → SEARCH_AGENT
- If unsure → SEARCH_AGENT

Return ONLY valid JSON:
{ "agent": "RAG_AGENT" } or { "agent": "SEARCH_AGENT" }
"""

        response = self.router_llm.invoke(
            router_prompt + f"\nUser Query: {query}"
        ).content.strip()

        try:
            decision = json.loads(response)
            agent = decision.get("agent", "SEARCH_AGENT")
            if agent not in ["RAG_AGENT", "SEARCH_AGENT"]:
                return "SEARCH_AGENT"
            return agent
        except Exception:
            return "SEARCH_AGENT"

    def route_and_execute(self, query: str) -> str:
        """
        Routes query to the correct agent and guarantees a string response.
        """

        print(f"\n🔍 UNIVERSAL ROUTING: '{query}'")

        agent = self.select_agent(query)
        print(f"   → MASTER AGENT DECISION → {agent}")

        try:
            if agent == "RAG_AGENT":
                result = self.rag_agent.execute(query)
            else:
                result = self.search_agent.execute(query)

            if result is None or not str(result).strip():
                return "⚠️ Sorry, I couldn't find an answer to that question."

            return str(result).strip()

        except Exception as e:
            return f"❌ Error processing request: {e}"


if __name__ == "__main__":
    master = SmartSupportMaster()

    print("""
============================================================
🤖 SMARTSUPPORTMASTER - AGENTIC EDITION
❌ Type 'quit' to exit
============================================================
""")

    while True:
        user_query = input("👤 You: ").strip()

        if user_query.lower() in ["quit", "exit", "bye"]:
            break

        response = master.route_and_execute(user_query)
        print(f"\n🤖 {response}")

