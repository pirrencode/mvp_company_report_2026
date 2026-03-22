# Company Offer Engine

Company Offer Engine is a production-style Streamlit MVP that turns a short client intake form into a complete sales offer pack.

## Features

- Clean Streamlit UI for client intake
- Multi-step agentic workflow:
  1. Client research from provided inputs
  2. Likely business pain points
  3. Service positioning strategy
  4. Three pricing tiers
  5. Tailored proposal
  6. Follow-up email draft
  7. QA/refinement pass for clarity and persuasion
- OpenAI or Anthropic provider support
- API keys via Streamlit secrets or environment variables
- Structured output in copy-friendly sections (`st.code` has a built-in copy button)
- Modular codebase with editable prompt templates

## Project Structure

```bash
.
├── app.py
├── llm.py
├── prompts.py
├── requirements.txt
├── ui.py
└── workflow.py
```

## Quickstart (Local)

### 1) Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2) Configure API access

Use either `.streamlit/secrets.toml` or environment variables.

#### Option A: Streamlit secrets (recommended)

Create `.streamlit/secrets.toml`:

```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "your_openai_key"
OPENAI_MODEL = "gpt-4.1-mini"

# OR
# LLM_PROVIDER = "anthropic"
# ANTHROPIC_API_KEY = "your_anthropic_key"
# ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"
```

#### Option B: Environment variables

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_openai_key
export OPENAI_MODEL=gpt-4.1-mini

# OR
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_anthropic_key
export ANTHROPIC_MODEL=claude-3-5-sonnet-latest
```

### 3) Run

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to `GitHub.com`.
2. In Streamlit Community Cloud, create a new app from your repo.
3. Set entrypoint to `app.py`.
4. Add secrets in the Streamlit app settings (same keys as above).
5. Deploy.

## Prompt Editing

All prompt templates are in `prompts.py`. You can tune style, strictness, and structure without changing the workflow code.

## Notes

- This MVP intentionally keeps orchestration simple and transparent.
- Website analysis is inference-driven from user-provided context unless you extend the app with a web fetch layer.
