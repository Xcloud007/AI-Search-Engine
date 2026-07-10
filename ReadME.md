<div align="center">

# 🔍 XCloud Search — AI-Powered CLI Search Engine

### A terminal-based search engine that fetches real Google results and synthesises them into clean, intelligent answers using a free AI model — in under 5 seconds.

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-7C3AED?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-6D28D9?style=for-the-badge&logo=meta&logoColor=white)
![Serper](https://img.shields.io/badge/Serper-Google%20Search%20API-5B21B6?style=for-the-badge&logo=google&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-Command%20Line-4C1D95?style=for-the-badge&logo=windowsterminal&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-7C3AED?style=for-the-badge)

<br/>

![Free](https://img.shields.io/badge/Cost-100%25%20Free-8B5CF6?style=flat-square)
&nbsp;
![No Card](https://img.shields.io/badge/Credit%20Card-Not%20Required-6D28D9?style=flat-square)
&nbsp;
![Model](https://img.shields.io/badge/Model-Llama%203.3%2070B-5B21B6?style=flat-square)

</div>

---

## What Is This?

**XCloud Search** is a custom AI-powered search engine that runs entirely inside your terminal.

You type a question. It searches Google in real time via the Serper API. The raw results are fed to **Llama 3.3 70B** — a state-of-the-art open-source AI model running on Groq's ultra-fast infrastructure. The AI reads all the results, filters the noise, and hands you back one clean, sourced answer.

Think of it as your own personal research assistant living in your command line — no browser, no ads, no distractions.

Both services used (**Serper.dev** and **Groq**) are completely free with no credit card required.

---

## Features

- **Real Google results** — not a mock search; fetches live web results via Serper.dev
- **AI-synthesised answers** — Llama 3.3 70B reads all results and writes one clear response
- **5 answer modes** — switch how the AI responds based on what you need
- **Google Answer Box support** — captures direct answers when Google shows them
- **Colour-coded terminal UI** — purple-themed, clean, easy to read
- **Loading animations** — smooth spinner while searching and thinking
- **Smart error handling** — tells you exactly what went wrong in plain English
- **One-shot mode** — pass a query directly from the command line without entering interactive mode
- **Zero cost** — built entirely on free API tiers

---

## Answer Modes

| Mode | Command | What It Does |
|---|---|---|
| **Normal** | `/mode normal` | Balanced 3–5 sentence answer with source URLs (default) |
| **Brief** | `/mode brief` | One or two sentences — fastest possible answer |
| **Deep** | `/mode deep` | Detailed explanation with sections and bullet points |
| **ELI5** | `/mode eli5` | Explain Like I'm 5 — simple words, fun analogy |
| **Code** | `/mode code` | Technical focus with a working code example |

---

## Project Structure

```
ai-search-engine/
│
├── search.py           ← The entire engine (one file)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## Technologies Used

| Technology | Purpose | Cost |
|---|---|---|
| **Python 3.8+** | Core programming language | Free |
| **Groq API** | Runs Llama 3.3 70B for AI answers | Free (no card) |
| **Llama 3.3 70B** | Open-source AI model by Meta | Free via Groq |
| **Serper.dev** | Fetches real Google search results | Free (2500 queries) |
| **requests** | Sends HTTP requests to APIs | Free (open source) |
| **groq** | Official Groq Python client | Free (open source) |

---

## Installation & Setup

### Prerequisites

You need **Python 3.8 or higher** installed on your machine.

Check by running:
```bash
python --version
```

If you see `Python 3.x.x` you're ready. If not, download it from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation.

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Xcloud007/ai-search-engine.git
cd ai-search-engine
```

---

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Get Your Free API Keys

**Serper.dev** (2500 free Google searches/month)
1. Go to [serper.dev](https://serper.dev)
2. Click **"Get API Key"** → sign in with Google
3. Copy your API key from the dashboard

**Groq** (free AI inference)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up → **API Keys** → **Create new key**
3. Copy your key (starts with `gsk_...`)

---

### Step 4 — Set Your API Keys

**Windows:**
```cmd
setx SERPER_API_KEY "your_serper_key_here"
setx GROQ_API_KEY "your_groq_key_here"
```
> Close and reopen CMD after running `setx`.

**Mac / Linux:**
```bash
export SERPER_API_KEY="your_serper_key_here"
export GROQ_API_KEY="your_groq_key_here"
```

---

### Step 5 — Run It

```bash
python search.py
```

---

## Usage

### Interactive Mode

```bash
python search.py
```

### One-Shot Query

```bash
python search.py "what is the difference between AI and machine learning"
```

### All Commands

```
  /mode normal    Balanced answer (default)
  /mode brief     One-liner, fastest
  /mode deep      Detailed with sections
  /mode eli5      Simple language, fun analogy
  /mode code      Technical with code example
  /clear          Clear the terminal
  /help           Show all commands
  /quit           Exit
```

---

## How It Works

```
You type a question
        │
        ▼
  serper_search()
        │  Queries Google via Serper.dev
        │  Returns top 6 results
        ▼
  groq_answer()
        │  Combines question + results into one prompt
        │  Sends to Llama 3.3 70B on Groq
        │  AI synthesises a clean, sourced answer
        ▼
  print_answer()
        │  Displays formatted answer in terminal
        ▼
  Clean answer in under 5 seconds
```

---

## Example Session

```
  > what is reinforcement learning

  ── Web Sources ──────────────────────────────────────
  [1] Reinforcement Learning — Wikipedia
      https://en.wikipedia.org/wiki/Reinforcement_learning
      Reinforcement learning is an area of machine learning where
      an agent learns to make decisions by taking actions...

  ── AI Answer ────────────────────────────────────────
  Reinforcement Learning (RL) is a type of machine learning where an
  agent learns to make decisions by interacting with an environment.
  The agent takes actions, receives rewards or penalties based on the
  outcome, and gradually learns which actions lead to the best results
  — similar to how a human learns through trial and error.

  Sources: en.wikipedia.org/wiki/Reinforcement_learning
```

---

## Security Note

**Never commit your API keys to GitHub.**

This repository includes a `.gitignore` that excludes `.env` files. Always use environment variables (Step 4) to store your keys — they stay on your machine and never touch the codebase.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a **Pull Request**

### Ideas for Contributions

- Save search history to a local file
- Add `/summarise` command to fetch and summarise a URL
- Support for Ollama (fully local, offline AI)
- Export answers to markdown with `/export`
- Add a `/compare` mode to compare two search queries side by side

---

## License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

Built with Python · Groq · Serper.dev &nbsp;·&nbsp; by [Rupesh Sharma](https://github.com/Xcloud007)

⭐ If this was useful to you, consider starring the repository

</div>
