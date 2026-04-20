<div align="center">

<br />

```
██╗    ██╗███████╗ █████╗ ██╗   ██╗███████╗
██║    ██║██╔════╝██╔══██╗██║   ██║██╔════╝
██║ █╗ ██║█████╗  ███████║██║   ██║█████╗  
██║███╗██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  
╚███╔███╔╝███████╗██║  ██║ ╚████╔╝ ███████╗
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
```

# 🧵 Weave — Agentic AI Coding Tool

**Describe what you want. Weave plans, architects, codes, reviews, and ships it.**

<br />

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-1DB954?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br />

> *Weaving agents into code — thread by thread.*

</div>

---

## ✨ What is Weave?

Weave is a **multi-agent AI coding system** that transforms a single natural language prompt into a fully functional project. Powered by LangGraph and Groq's LLaMA 3.3 70B, it orchestrates a pipeline of specialized agents — each responsible for a distinct phase of software development.

No boilerplate. No back-and-forth. Just describe your idea and let Weave build it.

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════╗
║               USER PROMPT                                    ║
║    "Build a modern todo app in HTML CSS JS"                  ║
╚══════════════════════════╦═══════════════════════════════════╝
                           ▼
              ┌────────────────────────┐
              │   📋  PLANNER          │
              │  Analyzes requirements │
              │  Picks project type    │
              │  Creates project plan  │
              └────────────┬───────────┘
                           ▼
              ┌────────────────────────┐
              │   🏗️  ARCHITECT        │
              │  Breaks plan into tasks│
              │  Orders by dependency  │
              │  Specifies file paths  │
              └────────────┬───────────┘
                           ▼
              ┌────────────────────────┐
              │   📝  CODER  (loop)    │
              │  Executes each task    │
              │  Reads existing files  │
              │  Retries up to 3×      │
              └────────────┬───────────┘
                           ▼
              ┌────────────────────────┐
              │   🔍  REVIEWER         │
              │  Checks correctness    │
              │  Security & practices  │
              └──────┬─────────────────┘
                     │
         ┌───────────┴──────────┐
         │   Issues found?      │
         ▼                      ▼
┌─────────────────┐   ┌─────────────────┐
│  🔧  CORRECTOR  │   │  🧪  TESTER     │
│  Fixes issues   │   │  Validates code │
│  Re-triggers    │   │  Syntax checks  │
│  reviewer  ─────┼──►│                 │
└─────────────────┘   └────────┬────────┘
                               ▼
              ┌────────────────────────────┐
              │   ✅  generated_project/   │
              │   Your project, ready.     │
              └────────────────────────────┘
```

---

## 🤖 Agent Pipeline

| # | Agent | Role |
|---|-------|------|
| 1 | **📋 Planner** | Converts raw prompt → structured project plan (name, stack, features, type) |
| 2 | **🏗️ Architect** | Decomposes plan → ordered implementation tasks with file specs |
| 3 | **📝 Coder** | Executes tasks iteratively; reads context; retries failed steps *(max 3×)* |
| 4 | **🔍 Reviewer** | Validates code quality, security, and best practices; flags issues |
| 5 | **🔧 Corrector** | Patches flagged issues and loops back to Reviewer |
| 6 | **🧪 Tester** | Runs type-specific validation and syntax checks |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/divyat2605/agentic-ai-coding-tool.git
cd weave
uv sync
```

### 2. Configure

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Build Something

```bash
# Default: HTML/CSS/JS project
python main.py "Build a modern todo app"

# Specify a project type
python main.py "Create a REST API for task management"  --type api
python main.py "Build a Python CLI tool for file org"   --type python
python main.py "Create a React analytics dashboard"     --type react
python main.py "Make a portfolio landing page"          --type static
```

Output is written to `generated_project/`. Open `index.html` in your browser.

---

## 📦 Supported Project Types

| Flag | Type | Description |
|------|------|-------------|
| *(default)* | `html_css_js` | Interactive web apps with vanilla JS |
| `--type python` | `python` | Python scripts, CLIs, utilities |
| `--type react` | `react` | Component-based React applications |
| `--type api` | `api` | RESTful backend APIs |
| `--type static` | `static` | Static marketing/portfolio sites |

---

## 💡 Example Prompts

```bash
python main.py "Create a calculator with a dark mode toggle"
python main.py "Build a responsive portfolio landing page"
python main.py "Make a quiz app with score tracking and a leaderboard"
python main.py "Build a Python CLI tool for bulk file renaming"
python main.py "Create a REST API for a task management system"
python main.py "Design a weather dashboard with animated icons"
```

---

## 🛠️ Tech Stack

| Technology | Role |
|------------|------|
| [**LangGraph**](https://langchain-ai.github.io/langgraph/) | Graph-based agent orchestration & state management |
| [**LangChain**](https://langchain.com) | LLM wrappers, tools, and prompt templates |
| [**Groq**](https://groq.com) | Ultra-fast LLaMA 3.3 70B inference |
| [**Pydantic**](https://docs.pydantic.dev) | Structured output validation between agents |

---

## ⚡ Key Features

| Feature | Details |
|---------|---------|
| 🔁 **Self-Correction Loop** | Reviewer → Corrector → Reviewer cycle until code is clean |
| 🔄 **Retry Logic** | Each coding step retries up to **3 times** before failing gracefully |
| 🗂️ **Multi-Project Support** | HTML, Python, React, API, and Static out of the box |
| 📡 **Real-Time Progress** | Emoji-prefixed live status output at every stage |
| 🎯 **Type-Aware Prompting** | Each agent adapts its instructions per project type |

---

## 📁 Project Structure

```
weave/
├── main.py               # Entry point & CLI arg parsing
├── agents/
│   ├── planner.py        # Requirement analysis → project plan
│   ├── architect.py      # Plan → ordered task list
│   ├── coder.py          # Task executor with retry logic
│   ├── reviewer.py       # Code quality & security checks
│   ├── corrector.py      # Issue fixer
│   └── tester.py         # Type-specific validation
├── graph/
│   └── workflow.py       # LangGraph state machine definition
├── generated_project/    # ← Your output lands here
├── .env.example
└── pyproject.toml
```

---

<div align="center">

Built with 🧵 by agents, for builders.

*If Weave helped you ship faster, drop a ⭐*

</div>