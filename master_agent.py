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

        # Router LLM (decision-only)
        self.router_llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )

        print("🤖 Master Agent: TRUE AGENTIC ROUTER Ready!")

    def select_agent(self, query: str) -> str:
        router_prompt = """
You are a MASTER ROUTER AGENT for a CUSTOMER SUPPORT SYSTEM.

Your job is to decide which agent can BEST answer the user's question.

AVAILABLE AGENTS:

1. RAG_AGENT
Use this agent for questions related to:
- Account management (password reset, login, 2FA, email settings)
- Billing, payments, subscriptions, refunds, invoices
- Orders, shipping, delivery, returns, warranty, exchange
- Product usage, troubleshooting, software updates, API access
- Company policies, privacy, GDPR, data export
- Support contact, escalation, priority support

IMPORTANT:
- These topics are ALWAYS assumed to be about the company's product
- Even if the company name is NOT mentioned

2. SEARCH_AGENT
Use this agent for:
- General knowledge
- Educational topics
- World facts
- Science and definitions
- How-to guides for public or third-party services
- Any question mentioning Gmail, Google, Netflix, Windows, Apple, etc.

CRITICAL RULES:
- "reset password", "forgot password", "cancel subscription",
  "track order", "billing issue" → RAG_AGENT
- If the user explicitly mentions another product or service → SEARCH_AGENT
- If the question is general or informational → SEARCH_AGENT
- If unsure → SEARCH_AGENT

Return ONLY valid JSON:
{ "agent": "RAG_AGENT" } OR { "agent": "SEARCH_AGENT" }
"""

        response = self.router_llm.invoke(
            router_prompt + f"\n\nUser Query: {query}"
        ).content.strip()

        try:
            decision = json.loads(response)
            return decision.get("agent", "SEARCH_AGENT")
        except:
            return "SEARCH_AGENT"

    def route_and_execute(self, query: str) -> str:
        print(f"\n🔍 UNIVERSAL ROUTING: '{query}'")
        agent = self.select_agent(query)
        print(f"   → MASTER AGENT DECISION → {agent}")

        if agent == "RAG_AGENT":
            return self.rag_agent.execute(query)

        return self.search_agent.execute(query)


if __name__ == "__main__":
    master = SmartSupportMaster()

    print("""
============================================================
🤖 SMARTSUPPORTMASTER - AGENTIC EDITION!
❌ Type 'quit' to exit
============================================================
""")

    while True:
        query = input("👤 You: ")
        if query.lower() in ["quit", "exit", "bye"]:
            break

        try:
            result = master.route_and_execute(query)
            print(f"\n🤖 {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
