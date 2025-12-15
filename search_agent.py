import os
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun


class SearchAgent:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0
        )

    def execute(self, query: str) -> str:
        search_results = self.search.run(query)

        prompt = f"""
You are a factual answering assistant.

Your task is to answer the user's question using the search results.

VERY IMPORTANT RULES:
- If the question asks for a FACT (who, what, when, where):
  - Give the EXACT answer in the FIRST sentence
  - Do NOT explain how to find the answer
  - Do NOT list steps
  - Do NOT give historical lists unless asked
- If the question is a HOW-TO:
  - Give clear, simple steps
- Be concise and accurate
- Do NOT say "as of my knowledge cutoff"

User Question:
{query}

Search Results:
{search_results}

Answer:
"""

        return self.llm.invoke(prompt).content.strip()
