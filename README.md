# 🤖 IT Ops AI Assistant — Week 3 Demo
## AI Pioneers — Cohort 1 | Mayank Chugh | 2026

A multi-turn IT Operations chatbot built with Python and Streamlit.  
Each provider has its own app file so you can compare APIs side by side.

**Concepts demonstrated:** API authentication, streaming responses, conversation memory, session state, system prompts, and domain personas.

---

## 🚀 Run locally

```bash
# 1. Activate your virtual environment
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
copy .env.example .env        # Windows
cp .env.example .env          # Mac/Linux
# Edit .env and add the API key for the provider you want to use

# 4. Run the app for your provider (examples below)
streamlit run app.py
```

Opens at: http://localhost:8501

---

## 🔌 Provider apps

Pick the file that matches your API key. All apps share the same UI, domains, and chat memory — only the backend changes.

| Provider | App file | Environment variable | Run command |
|----------|----------|----------------------|-------------|
| OpenAI (default) | `app.py` / `app-openai.py` | `OPENAI_API_KEY` | `streamlit run app.py` |
| Anthropic (Claude) | `app-claude.py` | `ANTHROPIC_API_KEY` | `streamlit run app-claude.py` |
| OpenRouter | `app-openrouter.py` | `OPENROUTER_API_KEY` | `streamlit run app-openrouter.py` |
| Groq | `app-groq.py` | `GROQ_API_KEY` | `streamlit run app-groq.py` |
| Mistral | `app-mistral.py` | `MISTRAL_API_KEY` | `streamlit run app-mistral.py` |
| Google Gemini | `app-gemini.py` | `GEMINI_API_KEY` | `streamlit run app-gemini.py` |
| Hugging Face | `app-huggingface.py` | `HF_TOKEN` | `streamlit run app-huggingface.py` |
| Ollama (local) | `app-ollama.py` | `OLLAMA_BASE_URL` *(optional)* | `streamlit run app-ollama.py` |

### Ollama (no cloud API key)

Ollama runs models on your machine. No paid API key is required.

```bash
ollama serve
ollama pull llama3.2
streamlit run app-ollama.py
```

Optional `.env` settings:

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
```

Model names in the sidebar must match models you have pulled locally (`ollama list`).

---

## ☁️ Deploy to Hugging Face Spaces

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **Streamlit** as the SDK
3. Upload the provider app you want (e.g. `app-groq.py` renamed to `app.py`) and `requirements.txt`
4. Go to **Settings → Secrets** and add the matching API key (see table above)
5. Your app goes live at: `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

> **Note:** Ollama is for local use only — it is not suitable for Hugging Face Spaces deployment.

---

## 🎓 What this demo teaches (Week 3 concepts)

| Concept | Where in the code |
|---------|-------------------|
| API authentication | `get_client()` — reads keys from `.env` |
| System prompts | `DOMAINS[selected]["system"]` — per-domain personas |
| Streaming | Provider-specific stream loop in each `app-*.py` |
| Multi-turn history | `st.session_state.messages` — full history sent every call |
| Session state | `st.session_state.*` — Streamlit session management |
| Token counting | Usage metadata shown under each response |
| Error handling | `try/except` for auth errors, rate limits, connection failures |

---

## 📁 Files

```
Charbot/
├── app.py                 ← OpenAI (default entry point)
├── app-openai.py          ← OpenAI
├── app-claude.py          ← Anthropic
├── app-openrouter.py      ← OpenRouter
├── app-groq.py            ← Groq
├── app-mistral.py         ← Mistral
├── app-gemini.py          ← Google Gemini
├── app-huggingface.py     ← Hugging Face Inference
├── app-ollama.py          ← Ollama (local)
├── requirements.txt       ← dependencies
├── .env.example           ← template for all API keys
└── README.md              ← this file
```

---

## 🔗 Mayank Chugh
- 📺 YouTube: [youtube.com/@itaienthusiast](https://youtube.com/@itaienthusiast)
- 💻 GitHub: [github.com/mayankchugh-learning](https://github.com/mayankchugh-learning)
- 💼 LinkedIn: [linkedin.com/in/mchugh77](https://linkedin.com/in/mchugh77)
- 📅 Book a call: [topmate.io/mayank_chugh](https://topmate.io/mayank_chugh)
- 🛒 Course: [mayanklearns.gumroad.com/l/aaskky](https://mayanklearns.gumroad.com/l/aaskky)
