"""
app-mistral.py — AI Pioneers Week 3 Demo
IT Operations Chatbot with Conversation Memory (Mistral)
Mayank Chugh | Azure OpenAI & GenAI Architecture | 2026

Run locally:
    streamlit run app-mistral.py

Deploy to Hugging Face Spaces:
    Upload this file + requirements.txt
    Add MISTRAL_API_KEY to Spaces secrets
"""

import os
from openai import AuthenticationError, OpenAI, RateLimitError
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IT Ops AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS — AI Pioneers dark theme ──────────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

    /* Root variables */
    :root {
        --navy:    #0A1628;
        --teal:    #0D9488;
        --teal-lt: #CCFBF1;
        --mint:    #14B8A6;
        --gold:    #F59E0B;
        --purple:  #7C3AED;
        --slate:   #475569;
        --slate-x: #94A3B8;
        --dark:    #0D1F35;
    }

    /* Global background */
    .stApp {
        background-color: var(--navy);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--dark) !important;
        border-right: 1px solid #1E3A5A;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #0D1F35;
        border-radius: 12px;
        border: 1px solid #1E3A5A;
        margin-bottom: 8px;
        padding: 4px 8px;
    }

    /* User message */
    [data-testid="stChatMessage"][data-testid*="user"] {
        border-left: 3px solid var(--teal);
    }

    /* Input box */
    [data-testid="stChatInput"] textarea {
        background-color: var(--dark) !important;
        border: 1px solid #1E3A5A !important;
        border-radius: 10px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 2px rgba(13,148,136,0.15) !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: transparent;
        border: 1px solid #1E3A5A;
        color: var(--slate-x);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        border-color: var(--teal);
        color: var(--teal);
        background-color: rgba(13,148,136,0.08);
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background-color: var(--dark);
        border: 1px solid #1E3A5A;
        border-radius: 8px;
        color: white;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: var(--dark);
        border: 1px solid #1E3A5A;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] p { color: var(--slate-x) !important; font-size: 11px !important; }
    [data-testid="stMetricValue"] { color: white !important; font-size: 22px !important; }

    /* Divider */
    hr { border-color: #1E3A5A !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--navy); }
    ::-webkit-scrollbar-thumb { background: #1E3A5A; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--teal); }

    /* Code font in messages */
    code {
        font-family: 'JetBrains Mono', monospace;
        background-color: rgba(13,148,136,0.12);
        border-radius: 4px;
        padding: 1px 5px;
        font-size: 12px;
        color: var(--teal-lt);
    }

    /* Header text colours */
    h1, h2, h3 { color: white !important; }
    p, li { color: var(--slate-x); }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: var(--dark);
        border: 1px solid #1E3A5A;
        border-radius: 10px;
    }

    /* Success/info boxes */
    .stAlert {
        background-color: var(--dark) !important;
        border-radius: 8px;
    }

    /* Badge pill styling */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    .badge-teal  { background: rgba(13,148,136,0.2); color: #5EEAD4; border: 1px solid rgba(13,148,136,0.3); }
    .badge-gold  { background: rgba(245,158,11,0.15); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); }
    .badge-purple{ background: rgba(124,58,237,0.15); color: #C4B5FD; border: 1px solid rgba(124,58,237,0.25); }
</style>
""", unsafe_allow_html=True)


# ── DOMAIN PRESETS ────────────────────────────────────────────────────────────
DOMAINS = {
    "🖥️  IT Operations": {
        "desc": "Windows Server, Azure, and enterprise infrastructure",
        "system": """You are a senior IT Operations specialist with 20 years of enterprise experience.
You specialise in Windows Server, Azure infrastructure, network operations, and IT service management.
Keep answers practical and concise — 3–5 sentences unless more detail is needed.
Always flag security risks and mention compliance implications where relevant.
Use bullet points for multi-step procedures.""",
        "starters": [
            "What patch cadence do you recommend for Windows Server 2019?",
            "Our database CPU has been at 95% for 10 minutes. What do I check first?",
            "How do I set up automated backups for Azure VMs?",
        ],
    },
    "🔒  Cybersecurity": {
        "desc": "Security operations, incident response, compliance",
        "system": """You are a senior cybersecurity analyst with expertise in SOC operations,
incident response, and enterprise security architecture.
Prioritise risk-based thinking. Flag any critical risks immediately.
Reference frameworks (NIST, ISO 27001, CIS Controls) where relevant.
Be direct — security advice should never be ambiguous.""",
        "starters": [
            "We've detected unusual outbound traffic on port 443. What are the first steps?",
            "How do I set up MFA across 500 users with minimal disruption?",
            "What's the most important thing to do in the first hour of a ransomware incident?",
        ],
    },
    "☁️  Cloud & DevOps": {
        "desc": "Azure, AWS, Kubernetes, CI/CD pipelines",
        "system": """You are a senior cloud architect and DevOps engineer specialising in
Azure and AWS infrastructure, Kubernetes, and CI/CD pipeline design.
Always consider cost optimisation alongside technical recommendations.
Prefer infrastructure-as-code approaches. Mention relevant managed services.
Keep answers actionable — what to do, not just what to consider.""",
        "starters": [
            "Our Kubernetes pods keep going into CrashLoopBackOff. Where do I start?",
            "What's the best way to implement blue-green deployments in Azure?",
            "How do I reduce our Azure spend without sacrificing reliability?",
        ],
    },
    "🗄️  Database & SQL": {
        "desc": "SQL Server, PostgreSQL, Azure SQL, performance tuning",
        "system": """You are a senior DBA with deep expertise in SQL Server, PostgreSQL, and Azure SQL.
You specialise in performance tuning, backup strategies, and high availability design.
Always ask about the scale (number of rows, concurrent users) before recommending a solution.
Mention index strategies, query plans, and blocking analysis when relevant.""",
        "starters": [
            "Our SSRS reports are timing out. The DBA says blocking spikes at 9am.",
            "What backup strategy do you recommend for a 2TB SQL Server database?",
            "How do I identify which queries are causing the most CPU pressure?",
        ],
    },
    "🌐  Networking": {
        "desc": "Cisco, firewalls, VPN, network architecture",
        "system": """You are a senior network engineer with expertise in enterprise networking,
Cisco infrastructure, firewall policy, VPN design, and SD-WAN.
Think in layers — always consider physical, logical, and security layers.
Reference RFC standards and vendor best practices where relevant.
Flag any single points of failure in proposed designs.""",
        "starters": [
            "Our VPN drops every 10 minutes. Wi-Fi is fine — only the VPN client disconnects.",
            "We're designing a network for 3 offices. What topology do you recommend?",
            "How do I implement zero-trust network access for remote workers?",
        ],
    },
    "✍️  Custom Domain": {
        "desc": "Set your own domain in the sidebar",
        "system": "You are a helpful IT professional assistant. Be concise and practical.",
        "starters": [
            "Tell me about your area of expertise.",
            "What are the most common problems you see in your domain?",
            "What would you recommend as a starting point for improving operations?",
        ],
    },
}

# ── SESSION STATE INITIALISATION ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "🖥️  IT Operations"
if "custom_system" not in st.session_state:
    st.session_state.custom_system = ""
if "model" not in st.session_state:
    st.session_state.model = "mistral-large-latest"

# ── API CLIENT ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client(api_key: str):
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.mistral.ai/v1",
    )

client = get_client(os.environ.get("MISTRAL_API_KEY", ""))

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / branding
    st.markdown("""
    <div style="padding: 8px 0 20px">
        <div style="font-size:11px; font-weight:600; color:#0D9488; letter-spacing:3px; margin-bottom:6px">AI PIONEERS · COHORT 1</div>
        <div style="font-size:22px; font-weight:700; color:white; line-height:1.2">IT Ops<br>AI Assistant</div>
        <div style="font-size:11px; color:#475569; margin-top:6px">Week 3 Demo · Mayank Chugh</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Domain selection
    st.markdown('<div style="font-size:11px; font-weight:500; color:#94A3B8; letter-spacing:2px; margin-bottom:8px">DOMAIN</div>', unsafe_allow_html=True)
    selected = st.selectbox(
        "Select domain",
        options=list(DOMAINS.keys()),
        index=0,
        label_visibility="collapsed",
        key="domain_select",
    )

    if selected != st.session_state.selected_domain:
        st.session_state.selected_domain = selected
        st.session_state.messages = []
        st.session_state.turn_count = 0
        st.rerun()

    domain_info = DOMAINS[selected]
    st.markdown(f'<div style="font-size:11px; color:#475569; margin-top:4px; margin-bottom:16px">{domain_info["desc"]}</div>', unsafe_allow_html=True)

    # Custom domain system prompt
    if selected == "✍️  Custom Domain":
        st.markdown('<div style="font-size:11px; font-weight:500; color:#94A3B8; letter-spacing:2px; margin-bottom:6px">SYSTEM PROMPT</div>', unsafe_allow_html=True)
        custom = st.text_area(
            "Custom system prompt",
            value=st.session_state.custom_system,
            height=120,
            placeholder="You are an expert in [your domain]...",
            label_visibility="collapsed",
        )
        st.session_state.custom_system = custom

    st.divider()

    # Model selector
    st.markdown('<div style="font-size:11px; font-weight:500; color:#94A3B8; letter-spacing:2px; margin-bottom:8px">MODEL</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        options=["mistral-large-latest", "mistral-small-latest", "open-mistral-nemo"],
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.model = model_choice

    st.divider()

    # Stats
    st.markdown('<div style="font-size:11px; font-weight:500; color:#94A3B8; letter-spacing:2px; margin-bottom:10px">SESSION STATS</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Turns", st.session_state.turn_count)
    with col2:
        st.metric("Tokens", f"{st.session_state.total_tokens:,}")

    # History size warning
    if len(st.session_state.messages) > 16:
        st.warning(f"⚠️ {len(st.session_state.messages)} messages in history. Consider clearing.", icon=None)

    st.divider()

    # Clear button
    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.turn_count = 0
        st.rerun()

    # About
    with st.expander("ℹ️  About this app"):
        st.markdown("""
        **Built with:**  
        `Python` · `Streamlit` · `Mistral API`

        **Concepts demonstrated:**  
        • API authentication  
        • Multi-turn conversation history  
        • System prompts & personas  
        • Streaming responses  
        • Session state management

        **Week 3 — AI Pioneers Cohort 1**  
        [github.com/mayankchugh-learning](https://github.com/mayankchugh-learning)
        """)


# ── MAIN CONTENT ──────────────────────────────────────────────────────────────

# Header
st.markdown(f"""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px">
    <div>
        <h1 style="margin:0; font-size:26px; font-weight:700">{selected.split("  ")[1] if "  " in selected else selected} Assistant</h1>
        <p style="margin:4px 0 0; font-size:13px">{domain_info["desc"]}</p>
    </div>
    <div>
        <span class="badge badge-teal">Memory ON</span>
        &nbsp;
        <span class="badge badge-gold">{model_choice.upper()}</span>
        &nbsp;
        <span class="badge badge-purple">Phase 2 · Week 3</span>
    </div>
</div>
""", unsafe_allow_html=True)

# API key check
if not client:
    st.markdown("""
    <div style="background:#0D1F35; border:1px solid #F59E0B; border-radius:12px; padding:20px; margin:20px 0">
        <div style="font-size:16px; font-weight:600; color:#F59E0B; margin-bottom:8px">⚠️  API Key Required</div>
        <div style="color:#94A3B8; font-size:13px; line-height:1.6">
            Set your <code>MISTRAL_API_KEY</code> environment variable to use this chatbot.<br><br>
            <strong style="color:white">Local:</strong> Copy <code>.env.example</code> to <code>.env</code> or run:<br>
            <code style="display:block; margin:8px 0; padding:8px; background:#0A1628; border-radius:6px">
            export MISTRAL_API_KEY=your-mistral-key-here
            </code>
            <strong style="color:white">Hugging Face Spaces:</strong> Add in Settings → Secrets.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Starter questions (shown when no conversation yet)
if not st.session_state.messages:
    st.markdown("""
    <div style="margin-bottom:20px">
        <div style="font-size:11px; font-weight:500; color:#94A3B8; letter-spacing:2px; margin-bottom:12px">TRY ASKING</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(domain_info["starters"]))
    for i, (col, starter) in enumerate(zip(cols, domain_info["starters"])):
        with col:
            if st.button(f"💬 {starter[:55]}{'...' if len(starter)>55 else ''}", key=f"starter_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": starter})
                st.rerun()

    st.divider()

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input(
    f"Ask your {selected.split('  ')[1] if '  ' in selected else 'IT'} question...",
    disabled=(not client)
)

if user_input:
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get system prompt
    if selected == "✍️  Custom Domain" and st.session_state.custom_system:
        system_prompt = st.session_state.custom_system
    else:
        system_prompt = domain_info["system"]

    # Build messages list for API — full history every call
    # IT analogy: stateless API, stateful YOU — send full transcript every time
    api_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Stream the response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        input_tokens = 0
        output_tokens = 0

        try:
            stream = client.chat.completions.create(
                model=st.session_state.model,
                max_tokens=1024,
                messages=api_messages,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")  # cursor effect

                if chunk.usage:
                    input_tokens = chunk.usage.prompt_tokens
                    output_tokens = chunk.usage.completion_tokens

            response_placeholder.markdown(full_response)

            # Update usage stats
            tokens_used = input_tokens + output_tokens
            st.session_state.total_tokens += tokens_used
            st.session_state.turn_count += 1

            # Show token count for this turn (educational for students)
            st.caption(f"↑ {input_tokens} tokens sent · {output_tokens} tokens received")

        except AuthenticationError:
            full_response = "❌ Invalid API key. Check your `MISTRAL_API_KEY` environment variable."
            response_placeholder.error(full_response)
        except RateLimitError:
            full_response = "⚠️ Rate limit reached. Wait a moment and try again."
            response_placeholder.warning(full_response)
        except Exception as e:
            full_response = f"❌ Error: {str(e)}"
            response_placeholder.error(full_response)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# Footer
st.markdown("""
<div style="margin-top:40px; padding-top:16px; border-top:1px solid #1E3A5A; display:flex; justify-content:space-between; align-items:center">
    <div style="font-size:11px; color:#334155">
        AI Pioneers — Cohort 1 · Week 3 Demo · Mayank Chugh
    </div>
    <div style="font-size:11px; color:#334155">
        youtube.com/@itaienthusiast · github.com/mayankchugh-learning
    </div>
</div>
""", unsafe_allow_html=True)
