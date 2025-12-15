from dotenv import load_dotenv
from master_agent import SmartSupportMaster
from init_db import create_vectorstore

load_dotenv()

def main():
    print("🔄 Initializing SmartSupportMaster...")
    create_vectorstore()
    agent = SmartSupportMaster()
    
    print("\n" + "="*60)
    print("🤖 SMARTSUPPORTMASTER - AGENTIC EDITION!")
    print("❌ Type 'quit' to exit")
    print("="*60)
    
    while True:
        query = input("\n👤 You: ").strip()
        if query.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
            
        try:
            response = agent.route_and_execute(query)
            print(f"\n🤖 {response}")
            print("-" * 80)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
