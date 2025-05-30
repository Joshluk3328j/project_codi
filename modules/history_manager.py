# programmers_assistant/modules/history_manager.py
import json
import os

# upload_history
HISTORY_FILE = "./modules/data/upload_history.json"

def save_history(history_data):
    """Save the upload history to a JSON file."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=2)

def load_history():
    """Load the upload history from a JSON file, or return an empty list if file doesn't exist or is corrupted."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def clear_history():
    """Delete the history file from disk."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# explanation history

EXPLANATION_HISTORY_FILE = "./modules/data/explanation_history.json"
AUDIO_DIR = "./modules/data/audio"
PDF_DIR = "./modules/data" 

def save_explanation_history(history):
    with open(EXPLANATION_HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_explanation_history():
    if os.path.exists(EXPLANATION_HISTORY_FILE):
        with open(EXPLANATION_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def clear_explanation_history():
    # Clear JSON history file
    with open(EXPLANATION_HISTORY_FILE, "w") as f:
        json.dump([], f)

    # Delete all MP3 files
    if os.path.exists(AUDIO_DIR):
        for file in os.listdir(AUDIO_DIR):
            if file.endswith(".mp3"):
                os.remove(os.path.join(AUDIO_DIR, file))

    # Optionally, delete all PDFs (if needed)
    for file in os.listdir(PDF_DIR):
        if file.startswith("explanation_") and file.endswith(".pdf"):
            os.remove(os.path.join(PDF_DIR, file))