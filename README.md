# 🪨 Shard

> Breaking prompts into components — An agentic AI builder. Describe what you want — Shard plans, architects, codes, reviews, and tests it.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-purple?style=flat-square)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER PROMPT                                     │
│                    "Build a modern todo app in HTML CSS JS"                │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  📋 PLANNER                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ • Analyzes requirements                                            │    │
│  │ • Creates project plan (name, description, techstack, features)   │    │
│  │ • Determines project type (HTML/JS, Python, React, API, Static)   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏗️ ARCHITECT                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ • Breaks plan into implementation tasks                            │    │
│  │ • Orders tasks by dependencies                                     │    │
│  │ • Specifies file paths, functions, classes, integrations          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  📝 CODER (loop)                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ • Iterates through each implementation task                       │    │
│  │ • Reads existing files for context                                │    │
│  │ • Writes complete file content using file tools                   │    │
│  │ • Retries failed steps up to 3 times                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔍 REVIEWER                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ • Reviews each generated file                                      │    │
│  │ • Checks for correctness, security, best practices                │    │
│  │ • Flags issues needing correction                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                         ┌────────┴────────┐
                         │  Issues found?  │
                         └────────┬────────┘
                    Yes           │           No
                         ┌────────┴────────┐
                         ▼                 ▼
              ┌──────────────────┐   ┌─────────────┐
              │ 🔧 CORRECTOR     │   │ 🧪 TESTER   │
              │ • Fixes issues   │   │ • Validates │
              │ • Re-triggers    │   │ • Checks    │
              │   review         │   │   syntax    │
              └────────┬─────────┘   └──────┬──────┘
                       │                    │
                       └────────┬───────────┘
                                ▼
              ┌─────────────────────────────────────┐
              │     ✅ GENERATED PROJECT            │
              │     (in generated_project/)         │
              └─────────────────────────────────────┘
```

---

## Workflow

| Stage | Agent | Description |
|-------|-------|-------------|
| 1 | **Planner** | Converts user prompt into structured project plan |
| 2 | **Architect** | Breaks plan into ordered implementation tasks |
| 3 | **Coder** | Executes tasks with retry logic (max 3 retries) |
| 4 | **Reviewer** | Validates code quality, flags issues |
| 5 | **Corrector** | Fixes flagged issues (loops back to reviewer) |
| 6 | **Tester** | Runs validation tests based on project type |

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/shard.git
cd shard
uv sync
cp .env.example .env  # add your GROQ_API_KEY
```

## Run

```bash
# Default: HTML/CSS/JS project
python main.py "Build a modern todo app"

# Specify project type
python main.py "Create a REST API" --type api
python main.py "Build a Python CLI tool" --type python
python main.py "Create a React dashboard" --type react
python main.py "Landing page" --type static
```

### Supported Project Types

| Type | Description |
|------|-------------|
| `html_css_js` | Web apps (default) |
| `python` | Python applications |
| `react` | React applications |
| `api` | REST APIs |
| `static` | Static websites |

Output lands in `generated_project/`. Open `index.html` in your browser.

---

## Example Prompts

```
"Create a calculator web application"
"Build a responsive portfolio landing page"
"Make a quiz app with score tracking"
"Build a Python CLI for file organization"
"Create a REST API for task management"
```

---

## Stack

| Technology | Purpose |
|------------|---------|
| **LangGraph** | Graph-based agent orchestration |
| **LangChain** | LLM wrapper & tools |
| **Groq** | LLaMA 3.3 70B inference |
| **Pydantic** | Structured output validation |

---

## Key Features

- ✅ **Self-Correction Loop** — Review → Fix → Re-review cycle
- ✅ **Retry Logic** — Up to 3 retries per coding step
- ✅ **Multi-Project Support** — HTML, Python, React, API, Static
- ✅ **Real-Time Progress** — Emoji-prefixed status output
- ✅ **Type-Specific Guidance** — Different prompts per project type