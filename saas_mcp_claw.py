#!/usr/bin/env python3
"""
SAAS-MCP Claw — Autonomous agent with jev (reasoning) + gpt6 (content).
Uses Explabs gateway: type-safe/jev-latest + openai/gpt-6-luna.
"""

import os, json, time, requests
from datetime import datetime

EXPLABS_KEY = os.environ.get("EXPLABS_API_KEY", "xpl_08b9a0678b55f04281447e9a993e538ffe1394c1")
ORG_ID = "69781319-690d-44d5-9ea1-ffebe31c0d8f"
BASE = "https://api.experientiallabs.ai"
HEADERS = {"Authorization": f"Bearer {EXPLABS_KEY}", "Content-Type": "application/json"}

def jev_decision(task, diff="", test=""):
    """jev-latest: TypeSafe reasoning via systemone."""
    payload = {
        "model": "type-safe/jev-latest",
        "state": {"task": task, "diff_summary": diff, "test_summary": test},
        "questions": {
            "decision": {
                "type": "choice",
                "instructions": "Decide: proceed, review, or block.",
                "criteria": {
                    "proceed": "All requirements met.",
                    "review": "Needs more info.",
                    "block": "Cannot proceed."
                }
            }
        }
    }
    r = requests.post(f"{BASE}/v1/systemone", headers=HEADERS, json=payload, timeout=15)
    if r.status_code == 200:
        return r.json().get("answers", {}).get("decision", "review")
    return "review"

def gpt6_chat(messages, reasoning="low"):
    """gpt-6-luna: Chat completion for content generation."""
    payload = {
        "model": "openai/gpt-6-luna",
        "messages": messages,
        "reasoning_effort": reasoning,
        "max_tokens": 1024
    }
    r = requests.post(f"{BASE}/api/v1/chat/completions", headers=HEADERS, json=payload, timeout=15)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    return "Error"

def run_claw(task, diff="", test=""):
    """Main loop: jev decides → gpt6 acts → result."""
    decision = jev_decision(task, diff, test)
    if decision != "proceed":
        return {"status": decision, "action": None}
    
    content = gpt6_chat([
        {"role": "system", "content": "Tu es SAAS-MCP Claw, agent autonome EON10. Agis."},
        {"role": "user", "content": task}
    ], reasoning="low")
    
    return {"status": "proceed", "action": content}

# Example usage
if __name__ == "__main__":
    result = run_claw("Render motion spot for friendises campaign")
    print(json.dumps(result, indent=2))
