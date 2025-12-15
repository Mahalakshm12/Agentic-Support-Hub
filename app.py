import streamlit as st
from master_agent import SmartSupportMaster
import time

# Page config
st.set_page_config(
    page_title="🔥 Agentic AI Hub", 
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CYBERPUNK WHITE CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
.stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #0f0f23 100%); }
.main-title { font-family: 'Orbitron', monospace !important; font-size: 4rem !important; font-weight: 900 !important; color: #ffffff !important; text-align: center; text-shadow: 0 0 30px rgba(255,255,255,0.5); animation: neonGlow 2s ease-in-out infinite alternate; }
.subtitle { font-family: 'Orbitron', monospace !important; font-size: 1.4rem !important; color: #ffffff !important; text-align: center; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
.neon-rag { background: linear-gradient(45deg, #ff00ff, #aa00ff); color: #ffffff !important; padding: 0.5rem 1.2rem !important; border-radius: 50px !important; font-weight: 700 !important; font-family: 'Orbitron', monospace !important; box-shadow: 0 0 20px rgba(255,0,255,0.5); border: 2px solid #ff00ff; }
.neon-search { background: linear-gradient(45deg, #00ff88, #00cc66); color: #ffffff !important; padding: 0.5rem 1.2rem !important; border-radius: 50px !important; font-weight: 700 !important; font-family: 'Orbitron', monospace !important; box-shadow: 0 0 20px rgba(0,255,136,0.5); border: 2px solid #00ff88; }
.stChatMessage { background: rgba(20,20,20,0.95) !important; border: 1px solid #444 !important; border-radius: 25px !important; color: #ffffff !important; }
.stMarkdown { color: #ffffff !important; }
.stProgress > div > div > div > div { background: linear-gradient(90deg, #00ff88, #00d4ff) !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0033 0%, #0a0a0a 100%) !important; border-right: 2px solid #ffffff !important; }
section[data-testid="stSidebar"] .stMarkdown { color: #ffffff !important; }
.stButton > button { color: #ffffff !important; border: 2px solid #ffffff !important; }
.stButton > button:hover { background-color: rgba(255,255,255,0.1) !important; box-shadow: 0 0 15px rgba(255,255,255,0.3) !important; }
@keyframes neonGlow { from { filter: drop-shadow(0 0 10px #ffffff); } to { filter: drop-shadow(0 0 20px #ffffff); } }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_master():
    return SmartSupportMaster()

master = get_master()

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, rgba(255,255,255,0.1) 0%, rgba(0,255,136,0.1) 50%, rgba(0,212,255,0.1) 100%); 
           padding: 2rem; border-radius: 20px; border: 2px solid #ffffff;'>
    <h1 class="main-title">🔥 AGENTIC AI HUB</h1>
    <p class="subtitle">Neural Router | RAG + Live Search | Infinite Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style='background: rgba(255,0,255,0.15); padding: 1.5rem; border-radius: 15px; border: 2px solid #ffffff; text-align: center; color: #ffffff;'>
        <h3 style='color: #ffffff !important; font-family: Orbitron;'>📚 KB NODES</h3>
        <h1 style='color: #ffffff !important; font-size: 2.5rem;'>27</h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='background: rgba(0,255,136,0.15); padding: 1.5rem; border-radius: 15px; border: 2px solid #ffffff; text-align: center; color: #ffffff;'>
        <h3 style='color: #ffffff !important; font-family: Orbitron;'>🌐 WEB NODES</h3>
        <h1 style='color: #ffffff !important; font-size: 2.5rem;'>LIVE</h1>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='background: rgba(0,212,255,0.15); padding: 1.5rem; border-radius: 15px; border: 2px solid #ffffff; text-align: center; color: #ffffff;'>
        <h3 style='color: #ffffff !important; font-family: Orbitron;'>⚡ LATENCY</h3>
        <h1 style='color: #ffffff !important; font-size: 2.5rem;'><1s</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h2 style='color: #ffffff !important; text-align: center; font-family: Orbitron;'>💬 NEURAL CHAT</h2>", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🔥 Neural Core Online\n\nAsk me company support OR world knowledge. I route perfectly."}
    ]

# Display messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**👤 YOU:** {message['content']}")
    else:
        with st.chat_message("assistant"):
            content = message["content"] if message["content"] else "No response"
            if "[RAG Agent]" in content:
                st.markdown('<span class="neon-rag">📚 RAG AGENT - Knowledge Base</span>', unsafe_allow_html=True)
                st.markdown(content.replace("[RAG Agent]", ""))
            elif "[Search Agent]" in content:
                st.markdown('<span class="neon-search">🌐 SEARCH AGENT - Live Web</span>', unsafe_allow_html=True)
                st.markdown(content.replace("[Search Agent]", ""))
            else:
                st.markdown(content)

# Chat input
if prompt := st.chat_input("🔍 Enter query (SmartSupport KB or World Search)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**👤 YOU:** {prompt}")

    with st.chat_message("assistant"):
        progress = st.progress(0)
        status = st.empty()
        
        status.markdown("**🔍 ROUTING...**")
        progress.progress(0.3)
        time.sleep(0.3)
        
        status.markdown("**⚙️ EXECUTING...**")
        progress.progress(0.8)
        time.sleep(0.3)
        
        try:
            response = master.route_and_execute(prompt)
            # ✅ FIXED: Safe None handling
            response_str = str(response) if response is not None else "No response from agent"
            progress.progress(1.0)
            status.markdown("**✅ ONLINE**")
            time.sleep(0.5)
        except Exception as e:
            response_str = f"❌ SYSTEM ERROR: {str(e)}"
        
        progress.empty()
        status.empty()
        
        # ✅ FIXED: Safe string checking
        if response_str and "[RAG Agent]" in response_str:
            st.markdown('<span class="neon-rag">📚 RAG AGENT</span>', unsafe_allow_html=True)
        elif response_str and "[Search Agent]" in response_str:
            st.markdown('<span class="neon-search">🌐 SEARCH AGENT</span>', unsafe_allow_html=True)
        st.markdown(response_str)

    st.session_state.messages.append({"role": "assistant", "content": response_str})

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff !important; font-family: Orbitron;'>🤖 AI CORE</h2>", unsafe_allow_html=True)
    
    if st.button("💥 RESET CHAT", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='color: #ffffff !important; font-family: Orbitron;'>
        <h3 style='color: #ffffff !important;'>🧠 RAG Agent</h3>
        <p style='color: #ffffff !important;'>SmartSupport KB<br>27 topics</p>
        <h3 style='color: #ffffff !important;'>🌐 Search Agent</h3>
        <p style='color: #ffffff !important;'>Live DDG Web<br>Real-time facts</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 2rem; color: #ffffff !important; font-family: Orbitron;'>
    <h3 style='color: #ffffff !important;'>Powered by 🔥 Neural Routing</h3>
    <p style='color: #ffffff !important;'>LangChain + Groq + Streamlit | 2025</p>
</div>
""", unsafe_allow_html=True)
