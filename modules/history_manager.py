# programmers_assistant/modules/history_manager.py

import os
import json
from typing import List, Dict

HISTORY_FILE = "project_codi/data/history.json"
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

def save(code: str, blocks: List[Dict[str, str]]) -> None:
    record = {"code": code, "explanations": blocks}
    history = load()
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-10:], f, indent=2)  # Keep last 10 records

def load() -> List[Dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
