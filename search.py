"""
Custom AI Search Engine
------------------------
Powered by:
  • Serper.dev  — real Google search results (FREE: 2500 queries, no credit card)
  • Groq API    — Llama 3.3 70B AI answers  (FREE: no credit card)

Setup:
  1. pip install requests groq
  2. Get free Serper key → https://serper.dev  (click "Get API Key", use Google login)
  3. Get free Groq key  → https://console.groq.com  (Sign up → API Keys)
  4. Run: python search.py

Usage:
  python search.py
  python search.py "what is reinforcement learning"
"""

import os
import sys
import textwrap
import time
from typing import Optional

try:
    import requests
except ImportError:
    sys.exit("[ERROR] Run: pip install requests groq")

try:
    from groq import Groq
except ImportError:
    sys.exit("[ERROR] Run: pip install requests groq")


# ── COLOURS ───────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"
WHITE  = "\033[97m"

def c(text, *codes): return "".join(codes) + str(text) + RESET
def wrap(text, width=80, indent=4):
    return textwrap.fill(text, width=width, subsequent_indent=" " * indent)


# ── API KEYS ──────────────────────────────────────────────────────────────────

def get_keys() -> tuple[str, str]:
    """
    Reads keys from environment variables, or prompts once.
    To avoid typing every time, run in CMD before launching:
        set SERPER_API_KEY=your_key
        set GROQ_API_KEY=your_key
    """
    serper_key = os.environ.get("SERPER_API_KEY", "").strip()
    groq_key   = os.environ.get("GROQ_API_KEY",   "").strip()

    if not serper_key:
        print(c("\n  Serper API key not found.", YELLOW))
        print(c("  FREE signup (no card): https://serper.dev → 'Get API Key'", DIM))
        serper_key = input(c("  Enter Serper API key: ", CYAN)).strip()

    if not groq_key:
        print(c("\n  Groq API key not found.", YELLOW))
        print(c("  FREE signup (no card): https://console.groq.com → API Keys", DIM))
        groq_key = input(c("  Enter Groq API key: ", CYAN)).strip()

    if not serper_key or not groq_key:
        sys.exit(c("\n  [ERROR] Both keys are required. Exiting.", RED))

    return serper_key, groq_key


# ── SERPER SEARCH ─────────────────────────────────────────────────────────────

def serper_search(query: str, api_key: str, count: int = 6) -> list[dict]:
    """Fetch real Google results via Serper.dev."""
    url     = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query, "num": count}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "?"
        if status == 401:
            print(c("\n  [ERROR] Invalid Serper API key.", RED))
        elif status == 429:
            print(c("\n  [ERROR] Serper rate limit hit. Wait a moment.", RED))
        else:
            print(c(f"\n  [ERROR] Serper API error {status}: {e}", RED))
        return []
    except requests.exceptions.ConnectionError:
        print(c("\n  [ERROR] No internet connection.", RED))
        return []
    except requests.exceptions.Timeout:
        print(c("\n  [ERROR] Serper request timed out.", RED))
        return []

    results = []
    data    = resp.json()

    # Answer box (when Google shows a direct answer)
    if "answerBox" in data:
        ab = data["answerBox"]
        results.append({
            "title":       ab.get("title", "Google Answer Box"),
            "url":         ab.get("link", ""),
            "description": ab.get("answer") or ab.get("snippet", ""),
        })

    # Organic results
    for r in data.get("organic", []):
        results.append({
            "title":       r.get("title", "No title"),
            "url":         r.get("link",  ""),
            "description": r.get("snippet", "No description available."),
        })

    return results[:count]


# ── GROQ AI ANSWER ────────────────────────────────────────────────────────────

def groq_answer(query: str, results: list[dict], client: Groq, mode: str = "normal") -> str:
    """Synthesise search results into a clean AI answer using Groq Llama 3.3."""

    if not results:
        context = "No web results found. Answer from your own knowledge."
    else:
        snippets = []
        for i, r in enumerate(results, 1):
            snippets.append(
                f"[{i}] {r['title']}\n    URL: {r['url']}\n    {r['description']}"
            )
        context = "\n\n".join(snippets)

    style = {
        "normal": "Give a clear answer in 3-5 sentences. End with the 2 most useful source URLs.",
        "brief":  "Answer in exactly 1-2 sentences. Be direct and concise.",
        "deep":   "Give a thorough explanation with sections and bullet points. Cite sources inline.",
        "eli5":   "Explain like I'm 5 years old. Use simple words and a fun analogy.",
        "code":   "Focus on code and technical aspects. Include a short working code example.",
    }.get(mode, "Give a clear answer in 3-5 sentences.")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI search assistant. "
                        "Synthesise web search results into a precise, helpful answer. "
                        "Never fabricate information not supported by the results. "
                        "Be direct — no filler, no padding."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nSearch results:\n{context}\n\nInstructions: {style}",
                },
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return c(f"[Groq error] {e}", RED)


# ── DISPLAY ───────────────────────────────────────────────────────────────────

def print_banner():
    banner = r"""
  ╔══════════════════════════════════════════════════════╗
  ║          XCLOUD SEARCH  ·  AI-Powered CLI            ║
  ║     Serper (Google)  +  Groq Llama 3.3 (70B)         ║
  ╚══════════════════════════════════════════════════════╝"""
    print(c(banner, PURPLE, BOLD))
    print(c("  Commands: /mode brief|deep|eli5|code|normal  /quit  /clear  /help\n", DIM))


def print_sources(results: list[dict]):
    if not results:
        return
    print(c("\n  ─── Web Sources ─────────────────────────────────────", DIM))
    for i, r in enumerate(results, 1):
        print(f"  {c(f'[{i}]', PURPLE)} {c(r['title'], WHITE)}")
        print(f"      {c(r['url'], DIM)}")
        desc = r["description"][:120] + "…" if len(r["description"]) > 120 else r["description"]
        print(f"      {c(desc, DIM)}\n")


def print_answer(answer: str):
    print(c("\n  ─── AI Answer ───────────────────────────────────────", CYAN))
    for line in answer.split("\n"):
        if line.strip():
            print("  " + wrap(line, width=76, indent=4))
        else:
            print()
    print()


def print_spinner(msg: str):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(6):
        for f in frames:
            sys.stdout.write(f"\r  {c(f, PURPLE)} {c(msg, DIM)}   ")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write("\r" + " " * 60 + "\r")


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────

def main():
    print_banner()
    serper_key, groq_key = get_keys()
    groq_client = Groq(api_key=groq_key)

    mode = "normal"
    print(c(f"  Ready. Mode: {mode}\n", GREEN))

    initial_query: Optional[str] = None
    if len(sys.argv) > 1:
        initial_query = " ".join(sys.argv[1:])

    while True:
        try:
            if initial_query:
                query = initial_query.strip()
                initial_query = None
                print(c(f"\n  > {query}", WHITE))
            else:
                query = input(c("  > ", PURPLE)).strip()
        except (KeyboardInterrupt, EOFError):
            print(c("\n\n  Goodbye.\n", DIM))
            break

        if not query:
            continue

        if query.lower() in ("/quit", "/exit", "quit", "exit"):
            print(c("\n  Goodbye.\n", DIM))
            break

        if query.lower() == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            print_banner()
            print(c(f"  Mode: {mode}\n", GREEN))
            continue

        if query.lower().startswith("/mode "):
            new_mode = query.split()[-1].lower()
            if new_mode in ("normal", "brief", "deep", "eli5", "code"):
                mode = new_mode
                print(c(f"  Mode set to: {mode}\n", GREEN))
            else:
                print(c("  Available modes: normal, brief, deep, eli5, code\n", YELLOW))
            continue

        if query.lower() == "/help":
            print(c("""
  Commands
  ────────
  /mode normal  — Balanced 3-5 sentence answer (default)
  /mode brief   — One-liner, fastest
  /mode deep    — Detailed with sections and bullet points
  /mode eli5    — Explain Like I'm 5
  /mode code    — Focus on code / technical detail
  /clear        — Clear the terminal
  /quit         — Exit
""", DIM))
            continue

        print_spinner("Searching Google via Serper ...")
        results = serper_search(query, serper_key)

        if results:
            print_sources(results)
        else:
            print(c("  [!] No web results — Groq will answer from its own knowledge.\n", YELLOW))

        print_spinner("Synthesising with Llama 3.3 ...")
        answer = groq_answer(query, results, groq_client, mode=mode)
        print_answer(answer)


if __name__ == "__main__":
    main()
